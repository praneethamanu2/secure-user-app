# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from .security import hash_password
from . import calculations
from .models import Calculation
from .schemas import CalculationCreate

def create_user(db: Session, user_in: schemas.UserCreate):
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user: models.User, username: str | None = None, email: str | None = None):
    if username:
        user.username = username
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user: models.User, new_password: str):
    # hash password and update
    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def create_calculation(db: Session, calc_in: CalculationCreate):
    # compute result using the calculation factory
    result = calculations.perform_calculation(calc_in.type, calc_in.a, calc_in.b)
    calc = Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def get_calculation(db: Session, calc_id: int):
    return db.query(Calculation).filter(Calculation.id == calc_id).first()


def get_calculation_stats(db: Session):
    """Return simple aggregate statistics about calculations."""
    total, avg_a, avg_b, avg_result = db.query(
        func.count(Calculation.id),
        func.avg(Calculation.a),
        func.avg(Calculation.b),
        func.avg(Calculation.result),
    ).one()

    # counts by type
    types = ["Add", "Sub", "Multiply", "Divide"]
    types = ["Add", "Sub", "Multiply", "Divide", "Power"]
    counts = {}
    for t in types:
        counts[t] = db.query(func.count(Calculation.id)).filter(Calculation.type == t).scalar() or 0

    return {
        "total_count": int(total or 0),
        "avg_a": float(avg_a) if avg_a is not None else None,
        "avg_b": float(avg_b) if avg_b is not None else None,
        "avg_result": float(avg_result) if avg_result is not None else None,
        "counts_by_type": counts,
    }


def get_calculation_history(db: Session, limit: int = 20, offset: int = 0):
    """Return recent calculations (most recent first) with total count."""
    total = db.query(func.count(Calculation.id)).scalar() or 0
    items = db.query(Calculation).order_by(Calculation.created_at.desc()).limit(limit).offset(offset).all()
    return {"total": int(total), "items": items}
