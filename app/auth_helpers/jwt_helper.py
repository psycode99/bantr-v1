from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.config import settings
from jose import jwt, JWTError

from app.db.models.user_model import User
from app.db.session import get_db

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_MINUTES = settings.expiration_minutes


def create_access_token(id: str):
    expires_in = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode = {"exp": expires_in, "user_id": id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_jwt(encoded_jwt: dict) -> dict:
    try:
        decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, ALGORITHM)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return decoded_jwt


def get_current_user(token, db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    user_id = int(payload.get('user_id'))
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user