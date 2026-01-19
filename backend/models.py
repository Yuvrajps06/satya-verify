from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class InputArticle(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_type: str  # 'text', 'url', 'image'
    content: str  # text content or URL or base64 image
    detected_language: Optional[str] = None
    original_text: Optional[str] = None  # Store original before translation
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Claim(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article_id: str
    claim_text: str
    claim_text_english: Optional[str] = None  # Translated version
    entities: List[Dict[str, str]] = []  # Named entities extracted
    claim_type: str  # 'factual', 'opinion', 'satire'
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SourceEvidence(BaseModel):
    source_name: str
    source_url: str
    relevant_text: str
    similarity_score: float  # 0-1
    credibility_score: float  # 0-100

class VerificationResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    claim_id: str
    verdict: str  # 'TRUE', 'FALSE', 'MISLEADING', 'UNVERIFIED'
    confidence: float  # 0-100
    explanation: str
    supporting_sources: List[SourceEvidence] = []
    contradicting_sources: List[SourceEvidence] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TrustedSource(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    domain: str
    credibility_score: float  # 0-100
    specialization: List[str]  # e.g., ['politics', 'health', 'tech']
    is_active: bool = True

class VerificationRequest(BaseModel):
    input_type: str  # 'text', 'url', 'image'
    content: str

class VerificationResponse(BaseModel):
    article_id: str
    detected_language: str
    original_text: str
    claims: List[Dict[str, Any]]  # List of claims with their verdicts
    overall_assessment: str
    timestamp: str
