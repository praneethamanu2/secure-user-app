from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from pathlib import Path

from .database import Base, engine, SessionLocal
from . import models, schemas, crud, calculations
from .security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .security import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

# Add security scheme for Swagger Authorize button
security = HTTPBearer()

app = FastAPI(
    title="Secure User App",
    description="JWT-authenticated calculations API with user registration/login",
    version="1.0.0"
)

# Mount static files at /static and also serve HTML from root
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Dependency to get the current user from the Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        scheme, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        uid: int | None = payload.get("uid")
        if username is None and uid is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # First try to find by username (most common). If username changed since
    # the token was issued, fall back to uid if present so users can still be
    # authenticated after updating username.
    user = None
    if username:
        user = crud.get_user_by_username(db, username)
    if not user and uid is not None:
        user = crud.get_user_by_id(db, uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
def read_root():
    static_dir = Path(__file__).parent / "static"
    return FileResponse(static_dir / "register.html")

@app.get("/register.html")
def get_register():
    static_dir = Path(__file__).parent / "static"
    return FileResponse(static_dir / "register.html")

@app.get("/login.html")
def get_login():
    static_dir = Path(__file__).parent / "static"
    return FileResponse(static_dir / "login.html")

@app.get("/dashboard.html")
def get_dashboard():
    static_dir = Path(__file__).parent / "static"
    return FileResponse(static_dir / "dashboard.html")


@app.get("/profile.html")
def get_profile():
    static_dir = Path(__file__).parent / "static"
    return FileResponse(static_dir / "profile.html")

@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(400, "Username already exists")
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already exists")
    return crud.create_user(db, user_in)


@app.post("/users/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return JWT token."""
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(400, "Username already exists")
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already exists")
    user = crud.create_user(db, user_in)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username, "uid": user.id}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }


@app.post("/users/login", response_model=schemas.TokenResponse)
def login_user(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login a user by verifying username and password, return JWT token."""
    user = crud.get_user_by_username(db, user_in.username)
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username, "uid": user.id}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }


@app.get("/users/me", response_model=schemas.UserRead)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@app.put("/users/me", response_model=schemas.UserRead)
def update_profile(update: schemas.UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # prevent duplicate username/email
    if update.username and crud.get_user_by_username(db, update.username) and update.username != current_user.username:
        raise HTTPException(status_code=400, detail="Username already exists")
    if update.email and crud.get_user_by_email(db, update.email) and update.email != current_user.email:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = crud.update_user(db, current_user, username=update.username, email=update.email)
    return user


@app.post("/users/me/change-password")
def change_password(payload: schemas.PasswordChange, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # verify current password
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    crud.change_user_password(db, current_user, payload.new_password)
    return {"detail": "Password changed"}


# Calculation BREAD Endpoints
@app.post("/calculations", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    """Add (POST) a new calculation."""
    try:
        return crud.create_calculation(db, calc_in)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/calculations/stats", response_model=schemas.CalculationStats)
def calculations_stats(db: Session = Depends(get_db)):
    """Return aggregate statistics about calculations."""
    return crud.get_calculation_stats(db)


@app.get("/reports/summary", response_model=schemas.CalculationStats)
def reports_summary(db: Session = Depends(get_db)):
    """Alias endpoint for calculation summary/reporting."""
    return crud.get_calculation_stats(db)


@app.get("/reports/history", response_model=schemas.ReportHistory)
def reports_history(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    """Return recent calculation history with pagination."""
    return crud.get_calculation_history(db, limit=limit, offset=offset)


@app.get("/calculations", response_model=list[schemas.CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    """Browse (GET) all calculations."""
    return db.query(models.Calculation).all()


@app.get("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    """Read (GET) a specific calculation by ID."""
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@app.put("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def edit_calculation(calc_id: int, calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    """Edit (PUT) an existing calculation."""
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    try:
        # Recompute result with new values
        result = calculations.perform_calculation(calc_in.type, calc_in.a, calc_in.b)
        calc.a = calc_in.a
        calc.b = calc_in.b
        calc.type = calc_in.type
        calc.result = result
        db.commit()
        db.refresh(calc)
        return calc
    except (ZeroDivisionError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    """Delete (DELETE) a calculation by ID."""
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return None
