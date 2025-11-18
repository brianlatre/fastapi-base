from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    nombre: str | None = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
