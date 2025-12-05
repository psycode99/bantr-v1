from sqlalchemy import Column, String, Integer
from app.db.base import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TIMESTAMP

class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    api_match_id = Column(Integer, unique=True, nullable=False)
    home_team = Column(String, nullable=True)
    away_team = Column(String, nullable=True)
    home_logo = Column(String, nullable=True)
    away_logo = Column(String, nullable=True)
    kickoff = Column(PG_TIMESTAMP(timezone=True), nullable=False)
    league = Column(String, nullable=False)
    league_code = Column(String, nullable=False)
    season = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    competition_logo = Column(String, nullable=False)
    country = Column(String, nullable=False)
    country_flag = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    winner = Column(String, nullable=True)
