from app.schemas import (
    PiiSanitizedBlock,
    RagResult,
    TailoredResume,
    VerificationResult,
    PdfArtifact
)
from app.pii.presidio_client import sanitize_text
from app.rag.retriever import retrieve_ats_constraints
from app.pdf.generator import generate_pdf
from app.persistence.state_manager import update_state
from app.llm.optimizer import optimize_resume
from app.llm.verifier import verify_resume



# NODE: PII SANITIZATION

def pii_node(state):
    sanitized_resume = sanitize_text(state.resume_text)
    sanitized_jd = sanitize_text(state.job_description)

    update_state(
        state.user_phone,
        sanitized_resume=sanitized_resume.sanitized_text,
        sanitized_jd=sanitized_jd.sanitized_text
    )

    return {
        "sanitized_resume": sanitized_resume.sanitized_text,
        "sanitized_jd": sanitized_jd.sanitized_text
    }



# NODE: RAG RETRIEVAL

def rag_node(state):
    result: RagResult = retrieve_ats_constraints(state.sanitized_jd)

    update_state(
        state.user_phone,
        rag_constraints=result.rules
    )

    return {"rag_constraints": result.rules}



# NODE: LLM OPTIMIZATION

def optimize_node(state):
    optimized: TailoredResume = optimize_resume(
        resume=state.sanitized_resume,
        job_description=state.sanitized_jd,
        constraints=state.rag_constraints
    )

    update_state(
        state.user_phone,
        optimized_resume=optimized.optimized_text
    )

    return {"optimized_resume": optimized.optimized_text}



# NODE: VERIFICATION / GUARDRAIL

def verify_node(state):
    verified: VerificationResult = verify_resume(
        original=state.sanitized_resume,
        optimized=state.optimized_resume
    )

    update_state(
        state.user_phone,
        verified_resume=verified.cleaned_text
    )

    return {"verified_resume": verified.cleaned_text}



# NODE: PDF GENERATION

def pdf_node(state):
    pdf: PdfArtifact = generate_pdf(
        user_phone=state.user_phone,
        text=state.verified_resume
    )

    update_state(
        state.user_phone,
        pdf_path=pdf.file_path
    )

    return {"pdf_path": pdf.file_path}
