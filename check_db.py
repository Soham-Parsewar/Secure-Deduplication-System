from backend.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    res = conn.execute(text("DESCRIBE files"))
    for row in res:
        print(row)
