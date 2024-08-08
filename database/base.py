from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings.config import Config

DB_URL = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

session = SessionLocal()
base = declarative_base()
