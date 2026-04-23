from cryptography.fernet import Fernet
import base64
import hashlib


def generate_key(file_hash):
    key = hashlib.sha256(file_hash.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_file(input_path, output_path, key):
    from cryptography.fernet import Fernet

    print("ENCRYPT FUNCTION CALLED")   # 👈 ADD THIS

    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        data = f.read()

    print("Original size:", len(data))

    encrypted = fernet.encrypt(data)

    with open(output_path, "wb") as f:
        f.write(encrypted)

    print("Encrypted saved at:", output_path)


def decrypt_file(input_path, output_path, key):
    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        data = f.read()

    decrypted = fernet.decrypt(data)

    with open(output_path, "wb") as f:
        f.write(decrypted)