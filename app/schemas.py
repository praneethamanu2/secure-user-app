# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict  # Contains user info without password


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: str

    @validator("type")
    def validate_type(cls, v):
        allowed = {"Add", "Sub", "Multiply", "Divide"}
        if v not in allowed:
            raise ValueError(f"type must be one of {allowed}")
        return v

    @validator("b")
    def validate_divisor(cls, v, values):
        # if type indicates division, ensure b is not zero
        t = values.get("type")
        if t == "Divide" and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: float | None = None
    created_at: datetime

    class Config:
        orm_mode = True
