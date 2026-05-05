import hashlib


# -------------------------
# FILE HASH (SHA-256)
# -------------------------
def generate_file_hash(file_path: str) -> str:
    """
    Generates SHA-256 hash of a file.
    Used for deduplication at file level.
    """

    hash_sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            # Read file in chunks (efficient for large files)
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()

    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")

    except Exception as e:
        raise Exception(f"Hashing failed: {str(e)}")


