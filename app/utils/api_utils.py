from fastapi import Header, HTTPException, status
from app.utils.errs import USER_ERROR_401_MESSAGE
from app.config import settings

BANTR_API_KEY = settings.bantr_api_key

def verify_api_key(api_key: str = Header(...)):
    if api_key != BANTR_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=USER_ERROR_401_MESSAGE)
