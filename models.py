from sqlalchemy import Column, Integer, String
from database import Base

# Define the User model to map to the 'users' table in the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
