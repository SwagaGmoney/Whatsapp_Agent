from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# TWILIO WEBHOOK SCHEMAS

class TwilioMessageInbound(BaseModel):
    """Incoming WhatsApp message from Twilio."""
    From: str
    Body: Optional[str] = ""
    NumMedia: int = 0
    MediaUrl0: Optional[str] = None
    MediaContentType0: Optional[str] = None
    MessageSid: str
    Timestamp: Optional[str] = None



# RESUME + JOB DESCRIPTION INGESTION

class ResumeInput(BaseModel):
    """Raw resume text or extracted PDF text."""
    user_phone: str
    resume_text: str
    source: str = Field("whatsapp", description="whatsapp | pdf | text")


class JobDescriptionInput(BaseModel):
    """Job description provided by the user."""
    user_phone: str
    job_description: str



# PII SANITIZATION

class PiiSanitizedBlock(BaseModel):
    """Output from Presidio analyzer + anonymizer."""
    sanitized_text: str
    entities_removed: List[str] = []



# RAG / QDRANT RETRIEVAL


class RagQuery(BaseModel):
    """Query to Qdrant for ATS parser rules."""
    query_text: str
    top_k: int = 5


class RagResult(BaseModel):
    """Retrieved ATS constraints from Qdrant."""
    rules: List[str]
    metadata: Optional[Dict[str, Any]] = None



# LLM OPTIMIZATION + VERIFICATION


class TailoredResume(BaseModel):
    """LLM‑generated optimized resume text."""
    optimized_text: str
    model_used: Optional[str] = None


class VerificationResult(BaseModel):
    """Self‑correction guardrail output."""
    cleaned_text: str
    removed_hallucinations: List[str] = []
    unauthorized_additions: List[str] = []



# FINAL PDF ARTIFACT

class PdfArtifact(BaseModel):
    """Final ATS‑compliant PDF metadata."""
    file_path: str
    file_size_kb: float
    delivered_to: str



# LANGGRAPH STATE MACHINE


class ConversationState(BaseModel):
    """Persistent state stored in PostgreSQL for LangGraph."""
    user_phone: str
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    sanitized_resume: Optional[str] = None
    sanitized_jd: Optional[str] = None
    rag_constraints: Optional[List[str]] = None
    optimized_resume: Optional[str] = None
    verified_resume: Optional[str] = None
    pdf_path: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# CELERY TASK PAYLOADS
class CeleryTaskPayload(BaseModel):
    """Payload sent to Celery worker."""
    user_phone: str
    message_sid: str
    event_type: str = Field(..., description="resume_uploaded | jd_uploaded")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CeleryTaskResult(BaseModel):
    """Worker result returned after processing."""
    user_phone: str
    status: str = Field(..., description="success | failed")
    detail: Optional[str] = None
    pdf_path: Optional[str] = None


# API RESPONSES
class ApiResponse(BaseModel):
    """Standardized API response wrapper."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
