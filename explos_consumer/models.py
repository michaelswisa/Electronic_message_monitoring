from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    ip_address = Column(String(255))
    created_at = Column(DateTime)

    location = relationship("Location", back_populates="email")
    device_info = relationship("DeviceInfo", back_populates="email")
    sentences = relationship("Sentence", back_populates="email")


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String(255))
    country = Column(String(255))
    email_id = Column(Integer, ForeignKey('emails.id'))

    email = relationship("Email", back_populates="location")


class DeviceInfo(Base):
    __tablename__ = 'device_infos'

    id = Column(Integer, primary_key=True)
    browser = Column(String(255))
    os = Column(String(255))
    device_id = Column(String(255))
    email_id = Column(Integer, ForeignKey('emails.id'))

    email = relationship("Email", back_populates="device_info")


class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)
    sentence = Column(String(255))
    email_id = Column(Integer, ForeignKey('emails.id'))

    email = relationship("Email", back_populates="sentences")
