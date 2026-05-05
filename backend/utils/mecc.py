from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import os

# -------------------------
# MECC CONFIG
# -------------------------
# Standard curve for base operations
curve = ec.SECP256R1()

# Server-side persistent keys (in a real app, these would be stored)
server_private_key = ec.generate_private_key(curve)
server_public_key = server_private_key.public_key()

def generate_mecc_keys():
    """
    Simulates MECC key generation as per paper:
    alpha_k = beta_k * rho_c (Public Key)
    o_k = alpha_k * beta_k * rho_c (Secret/Offset Key)
    """
    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    
    # Calculate offset key o_k (using shared secret logic)
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    
    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared_secret)
    ok = digest.finalize()
    
    return private_key, public_key, ok

def encrypt_mecc(data: bytes, public_key, ok: bytes):
    """
    Modified ECC Encryption:
    C1 = K * rho_c
    C2 = f + alpha_k + o_k
    """
    # ephemeral key K
    k_priv = ec.generate_private_key(curve)
    c1_pub = k_priv.public_key()
    
    # shared secret = k_priv * public_key
    shared = k_priv.exchange(ec.ECDH(), public_key)
    
    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared)
    digest.update(ok) # Adding o_k into the mix
    key = digest.finalize()[:16]
    
    # XOR with key (simplified "addition" for binary data)
    encrypted = bytes(a ^ b for a, b in zip(data, (key * (len(data) // 16 + 1))))
    
    # Return C1 (serialized) and C2
    return c1_pub, encrypted

def decrypt_mecc(c1_pub, encrypted_data: bytes, private_key, ok: bytes):
    """
    Modified ECC Decryption:
    f = C2 - beta_k * C1 - o_k
    """
    # shared secret = private_key * C1
    shared = private_key.exchange(ec.ECDH(), c1_pub)
    
    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared)
    digest.update(ok)
    key = digest.finalize()[:16]
    
    # XOR back
    decrypted = bytes(a ^ b for a, b in zip(encrypted_data, (key * (len(encrypted_data) // 16 + 1))))
    return decrypted