import hashlib

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB


# -------------------------
# Split file into blocks
# -------------------------
def chunk_file(file_path):
    chunks = []

    with open(file_path, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break

            chunk_hash = hashlib.sha256(data).hexdigest()
            chunks.append((chunk_hash, data))

    return chunks


# -------------------------
# MERKLE TREE (PoW)
# -------------------------
def merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]

    new_level = []

    for i in range(0, len(hashes), 2):
        left = hashes[i]
        right = hashes[i+1] if i+1 < len(hashes) else left

        combined = hashlib.sha256((left + right).encode()).hexdigest()
        new_level.append(combined)

    return merkle_root(new_level)