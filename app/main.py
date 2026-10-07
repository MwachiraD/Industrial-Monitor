from app.database import Base, engine
from app.models import Machine, Reading


Base.metadata.create_all(engine)