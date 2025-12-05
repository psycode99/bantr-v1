from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MatchResp(BaseModel):
    id: int 
    api_match_id: int
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_logo: Optional[str] = None
    away_logo: Optional[str] = None
    kickoff: datetime
    league: str
    league_code: str
    season: int
    status: str
    competition_logo: str
    country: str
    country_flag: str
    country_code: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    winner: Optional[str] = None

    class Config:
        orm_mode = True 