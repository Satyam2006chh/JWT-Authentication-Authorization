from passlib.context import CryptContext
from jose import jwt, JWTError
# jose is the library through which we can make the jwt token and then also verify it 
# jwt will basically encode and decode that token 
# jwterror will basically catch the errror if the token is invalid  
from datetime import datetime, timedelta
# datetime is used for the current time nd we r using th timedelta to manage the expiration for the jwt token 

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from .database import get_db
from .models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# CryptContext is basically password hashing manager object 
# bcrypt is an algorthm used to hash the passord but using it directly is very messy and hard 
# so passlib library ne ek wrapper diya h CryptContext  
# ye wrapper kya krta h ki - konsa alg use krna h manage krta h and hash generate krta h and pwd verify krta h and future me alg change krna easy krta h  
# deprecated = auto is basically an advanced techniquee which basically means that agar future me tum algorithm change kro and purane users ka hash old algorithm me ho to system automatically detect krke upgrade kr sakta h 
# so basically tum ek object bana rahe ho jiske paas .hash() and .verify() krkemethods h 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
# so basically this above line tells the fastapi that har protected request me authorization header se token nikal ke mujhe de dena 
# basically login krne ke baad user ko jwt token milta h and whenver he goes to any protected routes  then he has to send the token first 
# server ko us header se sirf token chaiye and instead of manually parsing it OAuth2PasswordBearer ye kam automatically krdeta h  

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user



# -----------------------
# now whats the work of this  ?  
# from fastapi.security import OAuth2PasswordBearer

# So basically this tells the fastapi that - 

# request ke header me jo bearer token ayega wo mujhe nikal ke dedo 
# bcoz 

# when the client logins we provide him the jwt token and phir wo har prottected route me request me bhejta h 
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Ye jo "Bearer <token>" part hai na —
# usko manually parse karna padta agar ye line na hoti.
# But OAuth2PasswordBearer ye kaam automatically karta hai.