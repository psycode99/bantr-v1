from fastapi import APIRouter, Depends, status, HTTPException, Header
from app.jobs.initial_season_sync import get_season_match_data
from app.config import settings
from app.utils.errs import USER_ERROR_401_MESSAGE

router = APIRouter(prefix='/v1/matches', tags=['Matches'])

BANTR_API_KEY = settings.bantr_api_key

def verify_api_key(api_key: str = Header(...)):
    if api_key != BANTR_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=USER_ERROR_401_MESSAGE)

@router.get('/season_match_data')
def get_match_data(api_key: str = Depends(verify_api_key)):
    leagues = {
        "Premier League": 2021,
        "Bundesliga": 2002,
        "La Liga": 2014,
        "Serie A": 2019,
        "Ligue 1": 2015,
        "UCL": 2001
    }
    data = get_season_match_data([league for league in leagues.values()], 2025)
    return data