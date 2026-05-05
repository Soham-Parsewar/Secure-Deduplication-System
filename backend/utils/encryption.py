from cryptography.fernet import Fernet
import base64
import hashlib
import os

def generate_convergent_key(file_content: bytes):
    """
    Convergent Encryption: Key is derived from file content hash.
    """
    file_hash = hashlib.sha256(file_content).digest()
    # Fernet keys must be 32 url-safe base64-encoded bytes
    return base64.urlsafe_b64encode(file_hash)

def encrypt_ce(data: bytes, key: bytes):
    """
    Layer 1: Convergent Encryption
    """
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_ce(encrypted_data: bytes, key: bytes):
    """
    Layer 1 Decryption
    """
    f = Fernet(key)
    return f.decrypt(encrypted_data)

def double_encrypt(file_content: bytes, mecc_pub, mecc_ok):
    """
    Paper Workflow: CE then MECC
    """
    # 1. CE
    ce_key = generate_convergent_key(file_content)
    ce_data = encrypt_ce(file_content, ce_key)
    
    # 2. MECC
    c1_pub, final_data = encrypt_mecc(ce_data, mecc_pub, mecc_ok)
    
    return final_data, c1_pub, ce_key

# We need to import mecc functions inside the file or pass them as args.
# For simplicity, I'll update mecc.py to be importable.
from backend.utils.mecc import encrypt_mecc, decrypt_mecc
