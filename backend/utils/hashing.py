import hashlib

def generate_file_hash(file_path):
    hash_sha512 = hashlib.sha512()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)

    return hash_sha512.hexdigest()