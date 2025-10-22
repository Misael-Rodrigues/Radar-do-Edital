from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel

SECRET_KEY = "chave_super_secreta_troque_isso"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: str
    password: str

def create_user(db: Session, user: UserCreate):
    hashed = pwd_context.hash(user.password)
    novo = models.User(email=user.email, hashed_password=hashed)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

