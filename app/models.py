from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint   
from sqlalchemy.orm import relationship
from app.database import Base


class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key = True)
    machine_id = Column(Integer , ForeignKey("machines.id"), nullable = False)
    temperature = Column(Float, nullable = False)
    timestamp = Column(DateTime, nullable = False)
    machine = relationship("Machine",  back_populates = "readings")
class Machine(Base):
    __tablename__ = "machines"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    model = Column(String, nullable = False)
    location = Column(String, nullable = False)
    readings = relationship( "Reading", back_populates = "machine")

    __table_args__ = (UniqueConstraint('name', 'location'),)