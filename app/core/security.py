from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# ---------- Password hashing (bcrypt) ----------
def hash_password(password: str) -> str:
    # bcrypt adds a random salt automatically
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# ---------- JWT access token ----------
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # "sub" (subject) is the standard JWT claim for "who is this token for"
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    # Raises JWTError if the token is invalid or expired
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
