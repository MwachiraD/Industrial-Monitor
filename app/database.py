from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
DATABASE_URL = "postgresql+psycopg://postgres:Peekaboo96@localhost:5432/industrial_monitor"

engine = create_engine(DATABASE_URL)
class Base(DeclarativeBase):
    pass