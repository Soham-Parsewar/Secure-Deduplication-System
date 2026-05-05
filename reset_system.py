from backend.database import engine
from sqlalchemy import text
import os

# 1. Reset Database Table
sql_drop = "DROP TABLE IF EXISTS files;"
sql_create = """
CREATE TABLE files (
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
    print("Dropping old table...")
    conn.execute(text(sql_drop))
    print("Creating new table with correct schema...")
    conn.execute(text(sql_create))
    conn.commit()

# 2. Reset CSV File
if os.path.exists("performance_results.csv"):
    os.remove("performance_results.csv")
    print("Performance CSV reset.")

print("System reset complete.")
