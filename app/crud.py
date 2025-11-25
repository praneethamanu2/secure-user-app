# app/crud.py
from sqlalchemy.orm import Session
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

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


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
