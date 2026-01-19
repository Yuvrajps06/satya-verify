import os
import re
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import logging
import json

load_dotenv()
logger = logging.getLogger(__name__)

class NLPService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY', '')
        
    async def detect_language(self, text: str) -> str:
        """
        Detect language of input text
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"lang-detect-{os.urandom(8).hex()}",
                system_message="You are a language detection system. Identify the primary language of the text."
            ).with_model("openai", "gpt-5.2")
            
            message = UserMessage(
                text=f"""Identify the primary language of this text. Respond with ONLY the language name (e.g., 'Hindi', 'English', 'Tamil', 'Telugu', 'Bengali', 'Kannada', 'Malayalam', 'Marathi', or 'Mixed').

Text: {text[:500]}"""
            )
            
            response = await chat.send_message(message)
            detected = response.strip() if response else "English"
            logger.info(f"Detected language: {detected}")
            return detected
            
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return "English"
    
    async def translate_to_english(self, text: str, source_language: str) -> str:
        """
        Translate regional text to English
        """
        if source_language.lower() == 'english':
            return text
            
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"translate-{os.urandom(8).hex()}",
                system_message="You are a professional translator specializing in Indian languages."
            ).with_model("openai", "gpt-5.2")
            
            message = UserMessage(
                text=f"""Translate the following {source_language} text to English. Maintain the meaning and context accurately. Return ONLY the translated text.

Text: {text}"""
            )
            
            response = await chat.send_message(message)
            if response:
                logger.info(f"Translated text from {source_language} to English")
                return response.strip()
            return text
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return text
    
    async def extract_claims(self, text: str) -> List[Dict[str, any]]:
        """
        Extract atomic factual claims from text
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"claims-{os.urandom(8).hex()}",
                system_message="You are a fact-checking expert that extracts verifiable claims from news articles."
            ).with_model("openai", "gpt-5.2")
            
            message = UserMessage(
                text=f"""Extract all factual claims from this text that can be verified. Ignore opinions and satire.

For each claim, provide:
1. The claim text
2. Claim type ('factual', 'opinion', or 'satire')
3. Key entities mentioned (people, places, organizations, dates)

Return as JSON array:
[
  {{
    "claim_text": "specific factual statement",
    "claim_type": "factual",
    "entities": [{{"type": "person", "value": "Name"}}]
  }}
]

Text:
{text}

Return ONLY the JSON array, no other text."""
            )
            
            response = await chat.send_message(message)
            
            if response:
                # Try to extract JSON from response
                try:
                    # Remove markdown code blocks if present
                    json_text = response.strip()
                    if json_text.startswith('```'):
                        json_text = re.sub(r'^```(?:json)?\n', '', json_text)
                        json_text = re.sub(r'\n```$', '', json_text)
                    
                    claims_data = json.loads(json_text)
                    
                    # Filter only factual claims
                    factual_claims = [
                        claim for claim in claims_data 
                        if claim.get('claim_type') == 'factual'
                    ]
                    
                    logger.info(f"Extracted {len(factual_claims)} factual claims")
                    return factual_claims
                    
                except json.JSONDecodeError as je:
                    logger.error(f"Failed to parse claims JSON: {je}")
                    # Fallback: treat entire text as one claim
                    return [{
                        "claim_text": text[:500],
                        "claim_type": "factual",
                        "entities": []
                    }]
            
            return []
            
        except Exception as e:
            logger.error(f"Claim extraction failed: {str(e)}")
            return []
    
    async def extract_named_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"ner-{os.urandom(8).hex()}",
                system_message="You are a named entity recognition system."
            ).with_model("openai", "gpt-5.2")
            
            message = UserMessage(
                text=f"""Extract all named entities from this text. Return as JSON array with type and value:
[
  {{"type": "person", "value": "Name"}},
  {{"type": "organization", "value": "Org Name"}},
  {{"type": "location", "value": "Place"}},
  {{"type": "date", "value": "Date"}}
]

Text: {text}

Return ONLY the JSON array."""
            )
            
            response = await chat.send_message(message)
            
            if response:
                try:
                    json_text = response.strip()
                    if json_text.startswith('```'):
                        json_text = re.sub(r'^```(?:json)?\n', '', json_text)
                        json_text = re.sub(r'\n```$', '', json_text)
                    
                    entities = json.loads(json_text)
                    logger.info(f"Extracted {len(entities)} entities")
                    return entities
                except json.JSONDecodeError:
                    logger.error("Failed to parse entities JSON")
                    return []
            
            return []
            
        except Exception as e:
            logger.error(f"NER failed: {str(e)}")
            return []
