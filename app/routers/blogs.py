from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import Blog, User
from app.schemas.blog import BlogCreate, BlogResponse, BlogListResponse

router = APIRouter(tags=["Blogs"])


# Helper: find a blog or return 404
def get_blog_or_404(id: int, db: Session) -> Blog:
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


# Helper: only the blog's owner or an admin can modify it
def check_owner_or_admin(blog: Blog, user: User):
    if blog.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to modify this blog")


# Create Blog (Protected API)
@router.post("/blogs", response_model=BlogResponse, status_code=201)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        owner_id=user.id,
    )

    # Adds data to blogs table
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


# Read/Fetch All Blogs (Public)
@router.get("/blogs", response_model=BlogListResponse)
def get_blogs(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=50),
    search: str = Query(default=""),
):
    query = db.query(Blog).options(joinedload(Blog.owner))

    if search:
        query = query.filter(Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page - 1) * limit
    blogs = query.order_by(Blog.id).offset(start).limit(limit).all()

    return {"page": page, "limit": limit, "total": total, "data": blogs}


# Read/Fetch Blog by Blog ID (Public)
@router.get("/blog/{id}", response_model=BlogResponse)
def get_blog(id: int, db: Session = Depends(get_db)):
    return get_blog_or_404(id, db)


# Update Blog API (owner or admin)
@router.put("/blog/{id}", response_model=BlogResponse)
def update_blog(id: int, blog: BlogCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing_blog = get_blog_or_404(id, db)
    check_owner_or_admin(existing_blog, user)

    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()

    return existing_blog


# Delete Blog API (owner or admin)
@router.delete("/blog/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    blog = get_blog_or_404(id, db)
    check_owner_or_admin(blog, user)

    db.delete(blog)
    db.commit()

    return {"message": "Blog deleted successfully!"}
