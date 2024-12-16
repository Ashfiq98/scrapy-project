from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_title = Column(String(255), nullable=False)
    rating = Column(Float)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String(255))
    price = Column(Float)
    image_url = Column(Text, nullable=True)


# Automatically create tables
Base.metadata.create_all(engine)
