from typing import Annotated, List
from fastapi import Response, status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.auth_helpers.jwt_helper import get_current_user
from app.db.models.user_model import User
from app.db.session import get_db
from app.schemas.user_schema import UserResp, UserUpdate
from app.utils.errs import USER_ERROR_404_MESSAGE, USER_ERROR_401_MESSAGE,  USER_ERROR_204_MESSAGE


router = APIRouter(prefix='/v1/users', tags=["User"])

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResp)
def get_current_user(current_user: Annotated[UserResp, Depends(get_current_user)], db: Session = Depends(get_db)):
    user_id = current_user.id
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_ERROR_404_MESSAGE)
    return user


@router.get('/all_users', status_code=status.HTTP_200_OK, response_model=List[UserResp])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=USER_ERROR_204_MESSAGE)
    return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_ERROR_404_MESSAGE)
    return user


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResp)
def update_user(id: int, user: UserUpdate, current_user: Annotated[UserResp, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=USER_ERROR_401_MESSAGE)
    user_check = db.query(User).filter_by(id=id).first()
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_ERROR_404_MESSAGE)
    update_stmt = update(User).where(User.id == id).values(**user.model_dump())
    db.execute(update_stmt)
    db.commit()
    db.refresh(user_check)
    return user_check
    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=USER_ERROR_401_MESSAGE)
    user_check = db.query(User).filter_by(id=id).first()
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_ERROR_404_MESSAGE)
    db.delete(user_check)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)