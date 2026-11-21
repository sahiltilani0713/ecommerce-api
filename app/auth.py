# This file handles password hashing, JWT tokens, and the get_current_user dependency

import os
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

# Secret key used to sign JWT tokens (read from environment, with a dev default)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Algorithm used to encode the JWT
ALGORITHM = "HS256"

# How long a token stays valid
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tells FastAPI where clients get their token (the login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Hash a plain-text password using bcrypt
def hash_password(password: str) -> str:
    # Convert the password to bytes, hash it, and return as a string
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Check if a plain-text password matches a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Create a JWT access token with an expiration time
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Set the token to expire after 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode and return the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Dependency that extracts and validates the current user from the JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Error to raise if the token is bad
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token and get the email from it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Look up the user in the database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
