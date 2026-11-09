from pydantic import BaseModel, EmailStr, Field, field_validator


# Input Schema: register
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_not_too_long(cls, value: str):
        # bcrypt only supports passwords up to 72 bytes
        if len(value.encode()) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return value


# Output Schema: never includes the password
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# Output Schema: login
class Token(BaseModel):
    access_token: str
    token_type: str
