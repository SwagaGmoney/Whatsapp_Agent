from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from presidio_analyzer import analyzer_engine
from app.schemas import (
    TwilioMessageInbound,
    ApiResponse,
    CeleryTaskPayload
)
from app.config import get_settings
from app.rate_limit import rate_limiter
from app.celery_app import celery_app
from app.twilio_utils import download_media_file
from app.persistence.state_manager import initialize_state_if_missing

from contextlib import asynccontextmanager
from app.pii.custom_recognizers import LinkedInRecognizer

import logging


settings = get_settings()
app = FastAPI(title=settings.APP_NAME)
logger = logging.getLogger(__name__)



# HEALTH CHECK
@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}

# custom recognizer 
@asynccontextmanager
async def lifespan(app):
    recognizer = LinkedInRecognizer()
    analyzer_engine.registry.add_recognizer(recognizer)
    print("Custom LinkedIn/GitHub/Portfolio recognizer loaded.")
    yield

app.router.lifespan_context = lifespan

# TWILIO WEBHOOK ENDPOINT
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    limited: bool = Depends(rate_limiter)
):
    """
    WhatsApp → Twilio → FastAPI webhook.
    Handles text messages and PDF uploads.
    """

    form = await request.form()
    data = TwilioMessageInbound(**form)

    user_phone = data.From
    logger.info(f"Incoming message from {user_phone}")

    # Rate limit check
    if limited:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Initialize LangGraph state if needed
    initialize_state_if_missing(user_phone)

    # Determine event type
    event_type = "resume_uploaded" if data.NumMedia > 0 else "jd_uploaded"

    # Handle PDF upload
    if data.NumMedia > 0:
        if "pdf" not in (data.MediaContentType0 or ""):
            raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

        pdf_path = download_media_file(
            url=data.MediaUrl0,
            content_type=data.MediaContentType0,
            user_phone=user_phone
        )

        logger.info(f"PDF saved for {user_phone}: {pdf_path}")

    # Enqueue Celery task
    payload = CeleryTaskPayload(
        user_phone=user_phone,
        message_sid=data.MessageSid,
        event_type=event_type
    )

    celery_app.send_task(
        "workers.process_message",
        args=[payload.model_dump()]
    )

    return JSONResponse(
        ApiResponse(
            success=True,
            message="Message received. Processing asynchronously.",
            data={"event_type": event_type}
        ).model_dump()
    )
