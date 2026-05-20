import requests
from app.config import get_settings
from app.schemas import PiiSanitizedBlock

settings = get_settings()


def analyze_text(text: str):
    """Send text to Presidio Analyzer."""
    url = f"{settings.PRESIDIO_ANALYZER_URL}/analyze"
    payload = {
        "text": text,
        "language": "en"
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


def anonymize_text(text: str, analysis_results):
    """Send analyzer results to Presidio Anonymizer."""
    url = f"{settings.PRESIDIO_ANONYMIZER_URL}/anonymize"

    payload = {
        "text": text,
        "analyzer_results": analysis_results,
        "anonymizers": {
            "DEFAULT": {"type": "replace", "new_value": "<PII>"}
        }
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()["text"]


def sanitize_text(text: str) -> PiiSanitizedBlock:
    """Full Presidio pipeline: analyze → anonymize."""
    analysis = analyze_text(text)
    sanitized = anonymize_text(text, analysis)

    removed_entities = list({item["entity_type"] for item in analysis})

    return PiiSanitizedBlock(
        sanitized_text=sanitized,
        entities_removed=removed_entities
    )
