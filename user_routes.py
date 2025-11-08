from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from auth import  create_access_token
from user_model import User
from database import get_db
from schemas import UserCreate
router = APIRouter(prefix="/users", tags=["Users"])
from fastapi.security import OAuth2PasswordRequestForm

# Register User

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password safely
        # hashed_pw = hash_password(user.password)

        # Create new user
        new_user = User(username=user.username, email=user.email, password=user.password)

        # Add to DB and commit
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully", "user": new_user}

    except HTTPException:
        # raise HTTP exceptions (like email already exists)
        raise
    except Exception as e:
        # catch any other errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


# Login User

@router.post("/login")
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

