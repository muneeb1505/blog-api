from fastapi import FastAPI

from app import models  # noqa: F401  (registers all tables)
from app.core.database import engine, Base
from app.routers import auth, blogs

# Create all registered tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.include_router(auth.router)
app.include_router(blogs.router)


# Home route
@app.get("/")
def home():
    return {"message": "Blog API Started...."}
