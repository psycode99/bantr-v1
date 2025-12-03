from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models.user_model import User