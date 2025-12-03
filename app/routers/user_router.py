from typing import Annotated
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth_helpers.jwt_helper import get_current_user
from app.db.models.user_model import User
from app.db.session import get_db
from app.schemas.user_schema import UserResp


router = APIRouter(prefix='/v1/users', tags=["User"])

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResp)
def get_current_user(current_user: Annotated[UserResp, Depends(get_current_user)], db: Session = Depends(get_db)):
    user_id = current_user.id
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user