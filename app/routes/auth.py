from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils.jwt_handler import create_access_token, get_current_user
from app.utils.passwd_handler import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=schemas.UserResponse)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email, 
        hashed_password=hashed_pwd 
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


          