import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fail fast: the app should not start without these
if not DATABASE_URL or not SECRET_KEY:
    raise RuntimeError("DATABASE_URL and SECRET_KEY must be set in the .env file")
