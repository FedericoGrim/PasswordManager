import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def GenerateSalt(length: int = 16) -> bytes:
    """Genera un salt casuale in byte"""
    return os.urandom(length)

def DeriveKey(password: str, salt: bytes) -> bytes:
    """Deriva una chiave AES dalla master password e dal salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def CriptPassword(masterPassword: str, plainPassword: str, salt: bytes) -> str:
    """Cripta una password usando AES-CBC + PKCS7 e restituisce Base64"""
    key = DeriveKey(masterPassword, salt)
    iv = os.urandom(16)  # IV casuale per CBC
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plainPassword.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    # Salvo IV + ciphertext insieme, entrambi in Base64
    return base64.b64encode(iv + ciphertext).decode()