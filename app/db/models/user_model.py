from sqlalchemy import Column, TIMESTAMP, String, Integer, func
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name  =  Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    profile_pic = Column(String, nullable=True)
    country = Column(String, nullable=True)
    fav_team = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    