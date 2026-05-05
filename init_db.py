from backend.database import engine
from sqlalchemy import text

# Create table if not exists with all required columns for the paper's implementation
sql = """
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_hash VARCHAR(256) UNIQUE NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    merkle_root VARCHAR(256),
    enc_key VARCHAR(512),
    c1_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("Database schema verified and updated for MECC + CE system.")