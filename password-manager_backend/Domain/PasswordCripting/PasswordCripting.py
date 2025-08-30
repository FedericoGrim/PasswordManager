import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


def DeriveKey(password: str, salt: bytes) -> bytes:
    """Deriva una chiave dalla master password e dal salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def hashPassword(masterPassword: str, plainPassword: str, salt: bytes) -> bytes:
    """Cripta una password usando master password + salt"""
    key = DeriveKey(masterPassword, salt)
    fernet = Fernet(key)
    return fernet.encrypt(plainPassword.encode())