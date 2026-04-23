from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from backend.utils.hashing import generate_file_hash
from backend.utils.dedup import check_duplicate, store_file_reference, get_existing_file
from backend.utils.encryption import generate_key, encrypt_file, decrypt_file
from backend.database import SessionLocal
from sqlalchemy import text

print("MAIN FILE LOADED")

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EDGE_STORAGE = os.path.join(BASE_DIR, "storage", "edge")
CLOUD_STORAGE = os.path.join(BASE_DIR, "storage", "cloud")

os.makedirs(EDGE_STORAGE, exist_ok=True)
os.makedirs(CLOUD_STORAGE, exist_ok=True)

print("EDGE PATH:", EDGE_STORAGE)
print("CLOUD PATH:", CLOUD_STORAGE)


# 🔹 Home
@app.get("/")
def home():
    return {"message": "Backend working"}


# 🔹 Upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        edge_path = os.path.join(EDGE_STORAGE, file.filename)

        # Save temporarily
        with open(edge_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Generate hash
        file_hash = generate_file_hash(edge_path)

        # ✅ Deduplication check
        if check_duplicate(file_hash):
            existing_path = get_existing_file(file_hash)
            os.remove(edge_path)

            return {
                "message": "Duplicate file detected",
                "existing_file": existing_path
            }

        # Encryption
        key = generate_key(file_hash)
        encrypted_filename = file.filename + ".enc"
        cloud_path = os.path.join(CLOUD_STORAGE, encrypted_filename)

        print("Encrypting:", edge_path)
        print("Saving to:", cloud_path)

        encrypt_file(edge_path, cloud_path, key)

        # Remove edge file (temporary)
        os.remove(edge_path)

        # Store in DB
        store_file_reference(file_hash, cloud_path)

        return {
            "message": "File stored successfully",
            "hash": file_hash
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return {"error": str(e)}


# 🔹 Download
@app.get("/download")
def download_file(file_hash: str, background_tasks: BackgroundTasks):
    encrypted_path = get_existing_file(file_hash)

    if not encrypted_path or not os.path.exists(encrypted_path):
        return {"error": "File not found"}

    key = generate_key(file_hash)

    decrypted_path = encrypted_path.replace(".enc", "_decrypted")

    decrypt_file(encrypted_path, decrypted_path, key)

    # Cleanup after response
    background_tasks.add_task(lambda: os.remove(decrypted_path) if os.path.exists(decrypted_path) else None)

    return FileResponse(
        decrypted_path,
        filename=file_hash + ".txt"
    )


# 🔹 Get all files
@app.get("/files")
def get_files():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT file_hash FROM files")).fetchall()
        return {"files": [row[0] for row in result]}
    finally:
        db.close()