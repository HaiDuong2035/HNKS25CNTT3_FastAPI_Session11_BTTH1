from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'mysql+pymysql://root:123456789@localhost:3306/parking_db'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()