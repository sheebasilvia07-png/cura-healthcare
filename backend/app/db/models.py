from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    CAREGIVER = "CAREGIVER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    medications = relationship("Medication", back_populates="patient")
    health_logs = relationship("HealthLog", back_populates="patient")

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)

    patient = relationship("User", back_populates="medications")

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    metric_type = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("User", back_populates="health_logs")
    