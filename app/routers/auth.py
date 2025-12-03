import email
from fastapi import Depends, APIRouter, Request, status
from oauth import google_oauth
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserResp
from db.models.user_model import User

router = APIRouter(prefix="/v1/auth", tags=['Auth'])

@router.get('/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await google_oauth.oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/callback', status_code=status.HTTP_200_OK, response_model=UserResp)
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await google_oauth.oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    user_check = db.query(User).filter_by(email=user_info.get('email')).first()
    if user_check:
        return user_check
    else:
        user_data = {
            "first_name": user_info.get('given_name'),
            "last_name": user_info.get('family_name'),
            "name": user_info.get('name'),
            "email": user_info.get('email'),
            "profile_pic": user_info.get('picture')
        }
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        return new_user