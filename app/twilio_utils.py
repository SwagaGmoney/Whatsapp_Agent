import os
import requests
from app.config import get_settings

settings = get_settings()


def download_media_file(url: str, content_type: str, user_phone: str) -> str:
    """
    Downloads a PDF sent via WhatsApp → Twilio.
    Ensures:
    - Only PDFs are accepted
    - File is stored under /data/resumes/{hash}/
    """

    if "pdf" not in content_type:
        raise ValueError("Only PDF files are supported")

    # Directory
    folder = f"data/resumes/{user_phone}"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/resume.pdf"

    # Twilio requires auth
    resp = requests.get(
        url,
        auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    )

    if resp.status_code != 200:
        raise RuntimeError("Failed to download media from Twilio")

    with open(file_path, "wb") as f:
        f.write(resp.content)

    return file_path
