from sqlalchemy import text
from backend.database import SessionLocal
import os
from backend.database import SessionLocal
from sqlalchemy import text
from backend.database import SessionLocal
# -------------------------
# Check duplicate file
# -------------------------
def check_duplicate(file_hash):
    db = SessionLocal()
    try:
        result = db.execute(
            text("SELECT 1 FROM files WHERE file_hash = :h"),
            {"h": file_hash}
        ).fetchone()

        return result is not None
    finally:
        db.close()


# -------------------------
# Store file metadata
# -------------------------
def store_file_reference(file_hash, file_path, merkle_root, enc_key):
    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO files (file_hash, file_path, merkle_root, enc_key)
        VALUES (:h, :p, :m, :k)
        """),
        {
            "h": file_hash,
            "p": file_path,
            "m": merkle_root,
            "k": enc_key
        }
    )

    db.commit()
    db.close()
    db.commit()
    db.close()
    db.commit()
    db.close()
# -------------------------
# Get file path
# -------------------------
def get_existing_file(file_hash):
    db = SessionLocal()
    try:
        result = db.execute(
            text("SELECT file_path FROM files WHERE file_hash = :hash"),
            {"hash": file_hash}
        ).fetchone()

        if result:
            return result[0]

        return None

    finally:
        db.close()