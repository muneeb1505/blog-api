from pydantic import BaseModel


# Input Schema
# Request body validation (author is taken from the logged-in user)
class BlogCreate(BaseModel):
    title: str
    content: str


# Output Schema
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

    class Config:
        from_attributes = True


# Output Schema for paginated list
class BlogListResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: list[BlogResponse]
