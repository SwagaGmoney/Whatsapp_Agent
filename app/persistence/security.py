import hashlib
import os
from cryptography.fernet import Fernet

# Load encryption key
FERNET_KEY = os.getenv("PII_ENCRYPTION_KEY")
cipher = Fernet(FERNET_KEY.encode())


# Hash phone number (non-reversible)
def hash_phone(phone: str) -> str:
    salt = os.getenv("PHONE_SALT", "default_salt")
    return hashlib.sha256(f"{salt}:{phone}".encode()).hexdigest()


# Encrypt text (reversible)
def encrypt(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()


# Decrypt text
def decrypt(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
