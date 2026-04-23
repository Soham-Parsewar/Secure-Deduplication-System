from sqlalchemy import text
from backend.database import SessionLocal


def check_duplicate(file_hash):
    db = SessionLocal()
    result = db.execute(
        text("SELECT file_path FROM files WHERE file_hash = :hash"),
        {"hash": file_hash}
    ).fetchone()
    db.close()
    return result is not None


def store_file_reference(file_hash, file_path):
    db = SessionLocal()
    try:
        # 🔍 Check before insert (IMPORTANT)
        existing = db.execute(
            text("SELECT * FROM files WHERE file_hash = :hash"),
            {"hash": file_hash}
        ).fetchone()

        if existing:
            print("Duplicate already exists in DB")
            return

        db.execute(
            text("INSERT INTO files (file_hash, file_path) VALUES (:hash, :path)"),
            {"hash": file_hash, "path": file_path}
        )
        db.commit()
        print("Inserted into DB")

    except Exception as e:
        print("DB ERROR:", e)

    finally:
        db.close()


def get_existing_file(file_hash):
    db = SessionLocal()
    result = db.execute(
        text("SELECT file_path FROM files WHERE file_hash = :hash"),
        {"hash": file_hash}
    ).fetchone()
    db.close()
    return result[0] if result else None