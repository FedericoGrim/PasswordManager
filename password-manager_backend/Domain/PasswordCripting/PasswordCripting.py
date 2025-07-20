from argon2.low_level import hash_secret_raw, Type
from os import urandom
import base64

@staticmethod
def HashMasterPassword(masterPassword: str) -> dict:
    """
    Hashes the master password using Argon2 with a random salt.

    Args:
        masterPassword (str): The master password to be hashed.

    Returns:
        dict: A dictionary containing the salt and the hashed password.

    Raises:
        Exception: If there is an error during the hashing process.
    """
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
    """
    Hashes the given password using Argon2 with the provided salt.

    Args:
        password (str): The password to be hashed.
        salt (str): The base64 encoded salt to be used for hashing.

    Returns:
        str: The base64 encoded hashed password.
        
    Raises:
        Exception: If there is an error during the hashing process.
    """
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