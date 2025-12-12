# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: constr(min_length=6)



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

    @field_validator("type")
    def validate_type(cls, v):
        allowed = {"Add", "Sub", "Multiply", "Divide", "Power"}
        if v not in allowed:
            raise ValueError(f"type must be one of {allowed}")
        return v

    @field_validator("b", mode="after")
    def validate_divisor(cls, v, info):
        # Support both pydantic v2 `info` object and older tests
        # that call the function with a plain dict for values.
        if isinstance(info, dict):
            t = info.get("type")
        else:
            t = getattr(info, "data", {}) and info.data.get("type") or None
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

    model_config = ConfigDict(from_attributes=True)


class CalculationStats(BaseModel):
    total_count: int
    avg_a: float | None = None
    avg_b: float | None = None
    avg_result: float | None = None
    counts_by_type: dict[str, int] = {}

    model_config = ConfigDict(from_attributes=True)


class ReportHistory(BaseModel):
    total: int
    items: list[CalculationRead] = []

    model_config = ConfigDict(from_attributes=True)
