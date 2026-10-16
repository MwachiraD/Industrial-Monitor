from app.database import Base, engine, SessionLocal
from app.models import Machine, Reading
from sqlalchemy.exc import IntegrityError


Base.metadata.create_all(engine)
try:
    with SessionLocal.begin() as db:
        boiler = Machine(
            name="Boiler_02", model="Thermal-X", location="Factory A")
        db.add(boiler)
except IntegrityError:
    print("Machine with this name and location already exists.")