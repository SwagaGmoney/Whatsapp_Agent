from app.pii.presidio_client import sanitize_text as presidio_sanitize
from app.persistence.security import encrypt
from app.schemas import PiiSanitizedBlock


def sanitize_and_encrypt(text: str) -> PiiSanitizedBlock:
    """
    Runs Presidio sanitization and encrypts the sanitized output.
    Ensures:
    - No raw PII is stored
    - Sanitized text is encrypted before DB persistence
    """
    sanitized_block = presidio_sanitize(text)

    encrypted_text = encrypt(sanitized_block.sanitized_text)

    return PiiSanitizedBlock(
        sanitized_text=encrypted_text,
        entities_removed=sanitized_block.entities_removed
    )
