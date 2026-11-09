"""
Create an admin user.
Run from the project root:  python -m scripts.create_admin
(Admins can't be created through /register on purpose.)
"""
from getpass import getpass

from app import models  # noqa: F401
from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models import User


def main():
    Base.metadata.create_all(bind=engine)

    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass("Admin password (min 8 chars): ")

    if len(username) < 3 or len(password) < 8 or len(password.encode()) > 72:
        print("Username must be 3+ chars and password 8-72 chars.")
        return

    db = SessionLocal()
    try:
        exists = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if exists:
            print("A user with that username or email already exists.")
            return

        db.add(User(username=username, email=email, hashed_password=hash_password(password), role="admin"))
        db.commit()
        print(f"Admin '{username}' created.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
