from fastapi import Depends, APIRouter, Request, status
from sqlalchemy.orm import Session

from app.auth_helpers.jwt_helper import create_access_token
from app.oauth import google_oauth
from app.db.session import get_db
from app.schemas.token_schema import TokenData
from app.db.models.user_model import User

router = APIRouter(prefix="/v1/auth", tags=['Auth'])

@router.get('/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await google_oauth.oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/callback', status_code=status.HTTP_200_OK, response_model=TokenData)
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await google_oauth.oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    user_check = db.query(User).filter_by(email=user_info.get('email')).first()
    if user_check:
        access_token = create_access_token(user_check.id)
        return {"access_token": access_token, "token_type": "bearer"}
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
        access_token = create_access_token(new_user.id)
        return {"access_token": access_token, "token_type": "bearer"}