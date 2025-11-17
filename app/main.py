from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, schemas, crud

app = FastAPI()

# Create tables on app startup (not at import)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Secure User App running"}

@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(400, "Username already exists")
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already exists")
    return crud.create_user(db, user_in)
