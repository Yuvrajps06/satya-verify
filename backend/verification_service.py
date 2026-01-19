import os
import aiohttp
import json
import re
from typing import List, Dict, Optional, Tuple
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import logging
import asyncio

load_dotenv()
logger = logging.getLogger(__name__)

class VerificationService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY', '')
        
        # Trusted Indian sources
        self.trusted_sources = {
            'PIB Fact Check': {
                'url': 'https://factcheck.pib.gov.in',
                'credibility': 95,
                'search_pattern': 'site:factcheck.pib.gov.in'
            },
            'Alt News': {
                'url': 'https://www.altnews.in',
                'credibility': 90,
                'search_pattern': 'site:altnews.in'
            },
            'BoomLive': {
                'url': 'https://www.boomlive.in/fact-check',
                'credibility': 90,
                'search_pattern': 'site:boomlive.in'
            },
            'The Hindu': {
                'url': 'https://www.thehindu.com',
                'credibility': 85,
                'search_pattern': 'site:thehindu.com'
            },
            'PTI': {
                'url': 'https://www.ptinews.com',
                'credibility': 88,
                'search_pattern': 'site:ptinews.com'
            }
        }
    
    async def generate_search_queries(self, claim: str) -> List[str]:
        """
        Generate search queries for a claim
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"query-gen-{os.urandom(8).hex()}",
                system_message="You are a search query generation expert for fact-checking."
            ).with_model("openai", "gpt-5.2")
            
            message = UserMessage(
                text=f"""Generate 3 effective search queries to verify this claim. Focus on key entities and facts.

Claim: {claim}

Return as JSON array: ["query1", "query2", "query3"]

Return ONLY the JSON array."""
            )
            
            response = await chat.send_message(message)
            
            if response:
                try:
                    json_text = response.strip()
                    if json_text.startswith('```'):
                        json_text = re.sub(r'^```(?:json)?\n', '', json_text)
                        json_text = re.sub(r'\n```$', '', json_text)
                    
                    queries = json.loads(json_text)
                    logger.info(f"Generated {len(queries)} search queries")
                    return queries[:3]
                except json.JSONDecodeError:
                    # Fallback: use the claim itself
                    return [claim]
            
            return [claim]
            
        except Exception as e:
            logger.error(f"Query generation failed: {str(e)}")
            return [claim]
    
    async def search_trusted_sources(self, query: str) -> List[Dict[str, any]]:
        """
        Simulate searching trusted sources (in production, would use actual search APIs)
        For MVP, we'll use LLM to generate realistic fact-check responses
        """
        try:
            # In a production system, this would:
            # 1. Use Google Custom Search API with site: filters
            # 2. Scrape the actual fact-check pages
            # 3. Extract relevant content
            
            # For MVP, we'll use LLM to simulate fact-check results
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"search-{os.urandom(8).hex()}",
                system_message="You are a fact-checking research assistant with knowledge of Indian news and fact-check databases."
            ).with_model("openai", "gpt-5.2")
            
            sources_list = ', '.join(self.trusted_sources.keys())
            
            message = UserMessage(
                text=f"""Based on your knowledge, provide fact-check information for this query from trusted Indian sources ({sources_list}).

Query: {query}

Return findings as JSON array:
[
  {{
    "source_name": "Source Name",
    "source_url": "https://example.com/article",
    "relevant_text": "Key findings about the claim",
    "stance": "supports" or "contradicts" or "neutral",
    "confidence": 0.85
  }}
]

If no reliable information is found, return empty array [].

Return ONLY the JSON array."""
            )
            
            response = await chat.send_message(message)
            
            if response:
                try:
                    json_text = response.strip()
                    if json_text.startswith('```'):
                        json_text = re.sub(r'^```(?:json)?\n', '', json_text)
                        json_text = re.sub(r'\n```$', '', json_text)
                    
                    results = json.loads(json_text)
                    
                    # Add credibility scores based on source
                    for result in results:
                        source_name = result.get('source_name', '')
                        for trusted_name, trusted_data in self.trusted_sources.items():
                            if trusted_name.lower() in source_name.lower():
                                result['credibility_score'] = trusted_data['credibility']
                                break
                        
                        if 'credibility_score' not in result:
                            result['credibility_score'] = 70  # Default
                    
                    logger.info(f"Found {len(results)} sources for query")
                    return results
                    
                except json.JSONDecodeError as je:
                    logger.error(f"Failed to parse search results: {je}")
                    return []
            
            return []
            
        except Exception as e:
            logger.error(f"Source search failed: {str(e)}")
            return []
    
    async def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between texts using embeddings
        """
        try:
            # Use OpenAI embeddings
            import openai
            client = openai.AsyncOpenAI(api_key=self.api_key, base_url="https://api.emergent.sh/v1")
            
            # Get embeddings
            response1 = await client.embeddings.create(
                input=text1[:8000],  # Limit length
                model="text-embedding-3-large"
            )
            
            response2 = await client.embeddings.create(
                input=text2[:8000],
                model="text-embedding-3-large"
            )
            
            # Extract embeddings
            emb1 = response1.data[0].embedding
            emb2 = response2.data[0].embedding
            
            # Calculate cosine similarity
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity
            
            similarity = cosine_similarity([emb1], [emb2])[0][0]
            
            logger.info(f"Calculated similarity: {similarity:.3f}")
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {str(e)}")
            # Fallback to simple text matching
            common_words = set(text1.lower().split()) & set(text2.lower().split())
            return len(common_words) / max(len(text1.split()), len(text2.split()), 1) * 0.5
    
    async def verify_claim(self, claim: str, claim_id: str) -> Dict[str, any]:
        """
        Main verification logic for a single claim
        """
        try:
            logger.info(f"Starting verification for claim: {claim[:100]}...")
            
            # Step 1: Generate search queries
            queries = await self.generate_search_queries(claim)
            
            # Step 2: Search trusted sources for each query
            all_sources = []
            for query in queries:
                sources = await self.search_trusted_sources(query)
                all_sources.extend(sources)
                await asyncio.sleep(0.5)  # Rate limiting
            
            # Step 3: Calculate similarities
            for source in all_sources:
                similarity = await self.calculate_semantic_similarity(
                    claim, 
                    source.get('relevant_text', '')
                )
                source['similarity_score'] = similarity
            
            # Step 4: Categorize sources
            supporting = [s for s in all_sources if s.get('stance') == 'supports' and s.get('similarity_score', 0) > 0.5]
            contradicting = [s for s in all_sources if s.get('stance') == 'contradicts' and s.get('similarity_score', 0) > 0.5]
            
            # Step 5: Determine verdict
            verdict, confidence, explanation = await self._determine_verdict(
                claim, supporting, contradicting
            )
            
            logger.info(f"Verdict for claim: {verdict} (confidence: {confidence}%)")
            
            return {
                'claim_id': claim_id,
                'verdict': verdict,
                'confidence': confidence,
                'explanation': explanation,
                'supporting_sources': supporting[:3],  # Top 3
                'contradicting_sources': contradicting[:3]  # Top 3
            }
            
        except Exception as e:
            logger.error(f"Claim verification failed: {str(e)}")
            return {
                'claim_id': claim_id,
                'verdict': 'UNVERIFIED',
                'confidence': 0,
                'explanation': f"Verification failed due to technical error: {str(e)}",
                'supporting_sources': [],
                'contradicting_sources': []
            }
    
    async def _determine_verdict(
        self, 
        claim: str, 
        supporting: List[Dict], 
        contradicting: List[Dict]
    ) -> Tuple[str, float, str]:
        """
        Determine final verdict based on evidence
        """
        try:
            # Use LLM to analyze evidence and generate verdict
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"verdict-{os.urandom(8).hex()}",
                system_message="You are an expert fact-checker. Analyze evidence objectively and provide clear verdicts."
            ).with_model("openai", "gpt-5.2")
            
            supporting_text = json.dumps(supporting, indent=2) if supporting else "None"
            contradicting_text = json.dumps(contradicting, indent=2) if contradicting else "None"
            
            message = UserMessage(
                text=f"""Analyze this claim and evidence to provide a fact-check verdict.

Claim: {claim}

Supporting Evidence:
{supporting_text}

Contradicting Evidence:
{contradicting_text}

Provide verdict as JSON:
{{
  "verdict": "TRUE" or "FALSE" or "MISLEADING" or "UNVERIFIED",
  "confidence": 0-100,
  "explanation": "Clear explanation in 2-3 sentences"
}}

Guidelines:
- TRUE: Strong evidence supports, no credible contradictions
- FALSE: Strong evidence contradicts
- MISLEADING: Partially true but missing context or exaggerated
- UNVERIFIED: Insufficient evidence

Return ONLY the JSON object."""
            )
            
            response = await chat.send_message(message)
            
            if response:
                try:
                    json_text = response.strip()
                    if json_text.startswith('```'):
                        json_text = re.sub(r'^```(?:json)?\n', '', json_text)
                        json_text = re.sub(r'\n```$', '', json_text)
                    
                    result = json.loads(json_text)
                    
                    return (
                        result.get('verdict', 'UNVERIFIED'),
                        float(result.get('confidence', 50)),
                        result.get('explanation', 'Unable to determine verdict')
                    )
                    
                except json.JSONDecodeError:
                    pass
            
            # Fallback logic
            if len(contradicting) > len(supporting):
                return ('FALSE', 60, 'Multiple sources contradict this claim.')
            elif len(supporting) > len(contradicting):
                return ('TRUE', 60, 'Multiple sources support this claim.')
            else:
                return ('UNVERIFIED', 30, 'Insufficient evidence to verify this claim.')
                
        except Exception as e:
            logger.error(f"Verdict determination failed: {str(e)}")
            return ('UNVERIFIED', 0, f'Error during verification: {str(e)}')
