from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Database Engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


# DB Dependency - one session per request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
