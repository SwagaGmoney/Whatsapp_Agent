from celery import Celery
from app.graph.flow import build_graph
from app.persistence.state_manager import (
    get_state,
    initialize_state_if_missing,
    update_state
)
from app.twilio_utils import send_whatsapp_message, send_whatsapp_media
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "resume_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task(name="process_resume_pipeline")
def process_resume_pipeline(user_phone: str):
    """
    Runs the full LangGraph pipeline:
    PII → RAG → Optimize → Verify → PDF
    """

    # Ensure DB state exists
    initialize_state_if_missing(user_phone)

    # Load state from DB
    state = get_state(user_phone)
    if not state:
        send_whatsapp_message(user_phone, "❌ Error: Could not load your session.")
        return

    # Build LangGraph
    graph = build_graph()

    try:
        # Execute graph
        final_state = graph.invoke(state.dict())

        # Save final PDF path
        update_state(
            user_phone,
            pdf_path=final_state.get("pdf_path")
        )

        # Notify user
        send_whatsapp_message(
            user_phone,
            "✅ Your optimized resume is ready! Sending your PDF now."
        )

        # Send PDF
        send_whatsapp_media(
            user_phone,
            final_state["pdf_path"],
            caption="📄 Your ATS‑optimized resume"
        )

    except Exception as e:
        send_whatsapp_message(
            user_phone,
            f"❌ Something went wrong while processing your resume.\n\nError: {str(e)}"
        )
        raise e
