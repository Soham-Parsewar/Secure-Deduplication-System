from backend.database import engine

sql = """
USE dedup_db;

ALTER TABLE files
ADD COLUMN merkle_root VARCHAR(256);
"""

with engine.connect() as conn:
    conn.execute(sql)
    conn.commit()

print("DB updated")