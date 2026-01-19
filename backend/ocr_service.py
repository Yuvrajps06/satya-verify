import os
import base64
from typing import Optional
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY', '')
        
    async def extract_text_from_image(self, image_base64: str) -> Optional[str]:
        """
        Extract text from image using OpenAI Vision API
        """
        try:
            # Create chat instance for this request
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"ocr-{os.urandom(8).hex()}",
                system_message="You are an OCR system that extracts text from images accurately. Extract all visible text including any Indian language content."
            ).with_model("openai", "gpt-5.2")
            
            # Create image content
            image_content = ImageContent(image_base64=image_base64)
            
            # Create message with image
            message = UserMessage(
                text="Extract all text from this image. If it contains Indian language text (Hindi, Tamil, Telugu, Bengali, etc.), include it as-is. Return only the extracted text without any additional commentary.",
                file_contents=[image_content]
            )
            
            # Send and get response
            response = await chat.send_message(message)
            
            if response:
                logger.info(f"OCR extracted text length: {len(response)}")
                return response.strip()
            
            logger.warning("No text extracted from image")
            return None
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return None
    
    def is_valid_image_base64(self, data: str) -> bool:
        """
        Validate if string is valid base64 image
        """
        try:
            # Check if it starts with data:image prefix
            if data.startswith('data:image/'):
                return True
            # Try to decode
            base64.b64decode(data)
            return True
        except Exception:
            return False
