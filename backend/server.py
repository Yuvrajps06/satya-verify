from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List

# Import models and services
from models import (
    InputArticle, Claim, VerificationResult, 
    VerificationRequest, VerificationResponse, TrustedSource
)
from ocr_service import OCRService
from nlp_service import NLPService
from verification_service import VerificationService
from credibility_service import CredibilityService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
ocr_service = OCRService()
nlp_service = NLPService()
verification_service = VerificationService()
credibility_service = CredibilityService()

# Create the main app without a prefix
app = FastAPI(title="SATYA-VERIFY API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@api_router.get("/")
async def root():
    return {
        "message": "SATYA-VERIFY API",
        "version": "1.0.0",
        "description": "AI-powered misinformation fact-checking for Indian regional news"
    }


@api_router.post("/verify", response_model=VerificationResponse)
async def verify_content(request: VerificationRequest):
    """
    Main endpoint to verify news content
    """
    try:
        logger.info(f"Received verification request: type={request.input_type}")
        
        # Step 1: Process input based on type
        if request.input_type == 'image':
            # Extract text from image using OCR
            logger.info("Processing image input with OCR")
            extracted_text = await ocr_service.extract_text_from_image(request.content)
            
            if not extracted_text:
                raise HTTPException(status_code=400, detail="Could not extract text from image")
            
            text_to_analyze = extracted_text
        
        elif request.input_type == 'url':
            # In production, would fetch and extract content from URL
            # For MVP, treat as text
            logger.info("Processing URL input (treating as text for MVP)")
            text_to_analyze = request.content
        
        else:  # text
            text_to_analyze = request.content
        
        if not text_to_analyze or len(text_to_analyze.strip()) < 10:
            raise HTTPException(status_code=400, detail="Content too short to analyze")
        
        # Step 2: Detect language
        detected_language = await nlp_service.detect_language(text_to_analyze)
        logger.info(f"Detected language: {detected_language}")
        
        # Step 3: Translate to English if needed
        original_text = text_to_analyze
        if detected_language.lower() != 'english':
            text_to_analyze = await nlp_service.translate_to_english(
                text_to_analyze, 
                detected_language
            )
            logger.info("Translated content to English")
        
        # Step 4: Save article to database
        article = InputArticle(
            input_type=request.input_type,
            content=request.content,
            detected_language=detected_language,
            original_text=original_text
        )
        
        article_dict = article.model_dump()
        article_dict['timestamp'] = article_dict['timestamp'].isoformat()
        await db.articles.insert_one(article_dict)
        logger.info(f"Saved article to database: {article.id}")
        
        # Step 5: Extract claims
        claims_data = await nlp_service.extract_claims(text_to_analyze)
        logger.info(f"Extracted {len(claims_data)} claims")
        
        if not claims_data:
            # If no claims extracted, treat entire text as one claim
            claims_data = [{
                'claim_text': text_to_analyze[:500],
                'claim_type': 'factual',
                'entities': []
            }]
        
        # Step 6: Verify each claim
        verified_claims = []
        
        for claim_data in claims_data[:5]:  # Limit to 5 claims for MVP
            # Create claim object
            claim = Claim(
                article_id=article.id,
                claim_text=claim_data.get('claim_text', ''),
                claim_text_english=claim_data.get('claim_text', ''),
                entities=claim_data.get('entities', []),
                claim_type=claim_data.get('claim_type', 'factual')
            )
            
            # Save claim to database
            claim_dict = claim.model_dump()
            claim_dict['timestamp'] = claim_dict['timestamp'].isoformat()
            await db.claims.insert_one(claim_dict)
            
            # Verify the claim
            verification_result = await verification_service.verify_claim(
                claim.claim_text,
                claim.id
            )
            
            # Enhance sources with credibility data
            for source in verification_result.get('supporting_sources', []):
                credibility_service.analyze_source_reputation(source)
            
            for source in verification_result.get('contradicting_sources', []):
                credibility_service.analyze_source_reputation(source)
            
            # Save verification result
            result = VerificationResult(
                claim_id=claim.id,
                verdict=verification_result.get('verdict', 'UNVERIFIED'),
                confidence=verification_result.get('confidence', 0),
                explanation=verification_result.get('explanation', ''),
                supporting_sources=verification_result.get('supporting_sources', []),
                contradicting_sources=verification_result.get('contradicting_sources', [])
            )
            
            result_dict = result.model_dump()
            result_dict['timestamp'] = result_dict['timestamp'].isoformat()
            await db.verification_results.insert_one(result_dict)
            
            verified_claims.append({
                'claim_id': claim.id,
                'claim_text': claim.claim_text,
                'verdict': result.verdict,
                'confidence': result.confidence,
                'explanation': result.explanation,
                'supporting_sources': result.supporting_sources,
                'contradicting_sources': result.contradicting_sources
            })
        
        # Step 7: Generate overall assessment
        verdicts = [c['verdict'] for c in verified_claims]
        false_count = verdicts.count('FALSE')
        misleading_count = verdicts.count('MISLEADING')
        
        if false_count > len(verdicts) / 2:
            overall = "This content contains multiple false claims and is likely misinformation."
        elif false_count + misleading_count > len(verdicts) / 2:
            overall = "This content contains misleading or false information."
        elif verdicts.count('TRUE') > len(verdicts) / 2:
            overall = "This content appears to be largely factual based on available evidence."
        else:
            overall = "Unable to fully verify this content. Some claims lack sufficient evidence."
        
        logger.info(f"Verification complete. Overall: {overall}")
        
        return VerificationResponse(
            article_id=article.id,
            detected_language=detected_language,
            original_text=original_text[:500] + ('...' if len(original_text) > 500 else ''),
            claims=verified_claims,
            overall_assessment=overall,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@api_router.get("/history")
async def get_verification_history(limit: int = 20):
    """
    Get verification history
    """
    try:
        articles = await db.articles.find(
            {}, 
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        return {"history": articles, "count": len(articles)}
    except Exception as e:
        logger.error(f"Failed to fetch history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")


@api_router.get("/sources")
async def get_trusted_sources():
    """
    Get list of trusted sources
    """
    try:
        sources = credibility_service.get_trusted_sources_list()
        return {"sources": sources, "count": len(sources)}
    except Exception as e:
        logger.error(f"Failed to fetch sources: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch sources")


@api_router.get("/stats")
async def get_statistics():
    """
    Get platform statistics
    """
    try:
        total_articles = await db.articles.count_documents({})
        total_claims = await db.claims.count_documents({})
        total_verifications = await db.verification_results.count_documents({})
        
        # Verdict distribution
        verdicts = await db.verification_results.find(
            {}, 
            {"verdict": 1, "_id": 0}
        ).to_list(1000)
        
        verdict_counts = {
            'TRUE': 0,
            'FALSE': 0,
            'MISLEADING': 0,
            'UNVERIFIED': 0
        }
        
        for v in verdicts:
            verdict = v.get('verdict', 'UNVERIFIED')
            if verdict in verdict_counts:
                verdict_counts[verdict] += 1
        
        return {
            "total_articles": total_articles,
            "total_claims": total_claims,
            "total_verifications": total_verifications,
            "verdict_distribution": verdict_counts
        }
    except Exception as e:
        logger.error(f"Failed to fetch stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
