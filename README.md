## Live Demo
https://blog-api-ggn1.onrender.com/docs

# Blog API

A FastAPI + PostgreSQL blog API with real authentication (JWT) and role-based authorization.

## Project structure

```
app/
├── main.py            # creates the app, includes routers
├── dependencies.py    # get_current_user, require_admin
├── core/
│   ├── config.py      # reads .env
│   ├── database.py    # engine, session, get_db
│   └── security.py    # bcrypt hashing + JWT create/decode
├── models/            # SQLAlchemy tables (User, Blog)
├── schemas/           # Pydantic request/response models
└── routers/
    ├── auth.py        # /register, /login, /me, /users
    └── blogs.py       # blog CRUD
scripts/
└── create_admin.py    # creates the first admin user
```

## Run

```bash
pip install -r requirements.txt
cp .env.example .env            # then fill in your values
python -m scripts.create_admin  # create an admin (optional)
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and use the **Authorize** button after registering.

## Auth flow

1. `POST /register` - creates a user (role is always `user`), password stored as a bcrypt hash.
2. `POST /login` - username or email + password, returns a JWT access token (30 min).
3. Send `Authorization: Bearer <token>` on protected routes.
4. `get_current_user` decodes the token and loads the user from the DB.
5. `require_admin` allows only users with role `admin`.

## Permissions

| Action | Who |
|---|---|
| Read blogs | Anyone |
| Create blog | Logged-in user (author = their username) |
| Update / delete blog | Blog owner or admin |
| `GET /users` | Admin only |
