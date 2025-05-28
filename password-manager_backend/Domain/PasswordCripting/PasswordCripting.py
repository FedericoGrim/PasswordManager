from argon2.low_level import hash_secret_raw, Type
from os import urandom
import base64

def HashMasterPassword(masterPassword: str) -> dict:
    try:
        salt = urandom(16)
        hashPwd = hash_secret_raw(
            secret=masterPassword.encode('utf-8'),
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=2,
            hash_len=32,
            type=Type.ID
        )
        return base64.b64encode(salt).decode('utf-8'), base64.b64encode(hashPwd).decode('utf-8')
    except Exception as e:
        raise Exception(f"Errore durante hashing master password: {e}")

def hashPassword(password: str, salt: str) -> str:
    try:
        hashPwd = hash_secret_raw(
            secret=password.encode('utf-8'),
            salt=base64.b64decode(salt),
            time_cost=3,
            memory_cost=65536,
            parallelism=2,
            hash_len=32,
            type=Type.ID
        )
        
        return base64.b64encode(hashPwd).decode('utf-8')
    
    except Exception as e:
        raise Exception(f"Errore durante hashing password: {e}")