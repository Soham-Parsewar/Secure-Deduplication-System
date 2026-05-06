from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For local/EC2 Simple deployment use SQLite
DATABASE_URL = "sqlite:///./dedup_system.db"

# For AWS RDS MySQL, use this format instead:
# DATABASE_URL = "mysql+pymysql://root:PASSWORD@ENDPOINT:3306/dedup_db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)