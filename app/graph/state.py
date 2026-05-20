
from typing import Optional, List
from langgraph.graph import StateGraph, END
from pydantic import BaseModel


class GraphState(BaseModel):
    user_phone: str
    resume_text: Optional[str] = None
    job_description: Optional[str] = None
    sanitized_resume: Optional[str] = None
    sanitized_jd: Optional[str] = None
    rag_constraints: Optional[List[str]] = None
    optimized_resume: Optional[str] = None
    verified_resume: Optional[str] = None
    pdf_path: Optional[str] = None
