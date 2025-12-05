from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import or_, Date
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.jobs.initial_season_sync import get_season_match_data
from app.utils.api_utils import verify_api_key
from app.utils.errs import TODAY_MATCHES_ERROR_204_MESSAGE,  MATCH_ERROR_404_MESSAGE, TEAM_MATCH_ERROR_204_MESSAGE, LEAGUE_MATCHES_ERROR_204_MESSAGE, MATCHES_ERROR_204_MESSAGE
from app.schemas.match_schema import MatchResp
from app.db.models.match_model import Match

from typing import List
from datetime import date


router = APIRouter(prefix='/v1/matches', tags=['Matches'])

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[MatchResp])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).order_by(Match.kickoff.asc()).limit(20).all()
    if not matches:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=MATCHES_ERROR_204_MESSAGE)
    return matches


@router.get("/match/{id}", status_code=status.HTTP_200_OK, response_model=MatchResp)
def get_match(id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter_by(id=id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MATCH_ERROR_404_MESSAGE)
    return match


@router.get('/team/{team}', status_code=status.HTTP_200_OK, response_model=List[MatchResp])
def get_matches_for_team(team: str, db: Session = Depends(get_db)):
    team_matches = db.query(Match).filter(or_(Match.home_team.ilike(f"%{team}%"), Match.away_team.ilike((f"%{team}%")))).order_by(Match.kickoff.asc()).all()
    if not team_matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TEAM_MATCH_ERROR_204_MESSAGE)
    return team_matches


@router.get('/league/{league_code}', status_code=status.HTTP_200_OK, response_model=List[MatchResp])
def get_matches_for_league(league_code: str, db: Session = Depends(get_db)):
    league_matches = db.query(Match).filter(Match.league_code.ilike(league_code)).order_by(Match.kickoff).all()
    if not league_matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=LEAGUE_MATCHES_ERROR_204_MESSAGE)
    return league_matches


@router.get('/today', status_code=status.HTTP_200_OK, response_model=List[MatchResp])
def get_matches_today(db: Session = Depends(get_db)):
    today = date.today()
    today_matches = db.query(Match).filter(Match.kickoff.cast(Date) == today).order_by(Match.kickoff.asc()).all()
    if not today_matches:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TODAY_MATCHES_ERROR_204_MESSAGE)
    return today_matches


@router.get('/season_match_data')
def get_match_data(api_key: str = Depends(verify_api_key)):
    """
    To be ran just once at the beginning of a season or can tweak the leagues dict
    for specific competitions like the world cup. For auto scheduling will use
    an external cron job app to run it.
    """
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
