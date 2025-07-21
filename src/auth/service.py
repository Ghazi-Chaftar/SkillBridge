"""This module provides authentication services for the application"""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID, uuid4

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.auth.model import LoginRequest
from src.entities.user import User
from src.exceptions import AuthenticationError, DuplicateEmailError, DuplicatePhoneError, InvalidCrendentialError
from src.profiles.model import ProfileCreate
from src.profiles.service import create_profile

from .model import RegisterUserRequest, Token, TokenData

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {"sub": email, "id": str(user_id), "exp": datetime.now(timezone.utc) + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        return TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, register_user_request: RegisterUserRequest) -> None:
    try:
        existing_user = db.query(User).filter(User.email == register_user_request.email).first()
        if existing_user:
            logging.warning(f"Registration attempt with existing email: {register_user_request.email}")
            raise DuplicateEmailError(register_user_request.email)

        existing_user = db.query(User).filter(User.phone_number == register_user_request.phone_number).first()
        if existing_user:
            logging.warning(f"Registration attempt with existing phone number: {register_user_request.phone_number}")
            raise DuplicatePhoneError(register_user_request.phone_number)

        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            phone_number=register_user_request.phone_number,
            password_hash=get_password_hash(register_user_request.password),
        )
        db.add(create_user_model)
        db.commit()
        profile_data = ProfileCreate(user_id=create_user_model.id)
        create_profile(db, profile_data)

        logging.info(f"Successfully registered user: {register_user_request.email}")
    except DuplicateEmailError:
        # Re-raise DuplicateEmailError
        raise
    except Exception as e:
        logging.error(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
        raise


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]


def login_for_access_token(form_data: LoginRequest, db: Session) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise InvalidCrendentialError()
    token = create_access_token(user.email, user.id, timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    return Token(access_token=token, token_type="bearer")
