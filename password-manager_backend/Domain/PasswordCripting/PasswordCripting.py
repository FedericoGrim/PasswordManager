import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def DeriveKey(password: str, salt: bytes) -> bytes:
    """Deriva una chiave AES-256 da master password e salt (PBKDF2 con SHA256)"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def EncryptPassword(masterPassword: str, plainPassword: str, salt: bytes) -> str:
    """Cripta la password con AES-CBC compatibile con CryptoJS"""
    key = DeriveKey(masterPassword, salt)

    iv = os.urandom(16)

    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plainPassword.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # ritorna IV + ciphertext in Base64 (stesso schema che usi in TS)
    return base64.b64encode(iv + ciphertext).decode()


def GenerateSalt(length: int = 16) -> str:
    """Genera salt casuale in hex stile Postgres (con prefisso \\x)"""
    return "\\x" + os.urandom(length).hex()
