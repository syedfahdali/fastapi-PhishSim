from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import engine
from sqlalchemy.ext.declarative import declarative_base

# Declare the Base class
Base = declarative_base()

# Example User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    token = Column(String)

    # Relationship to the Campaign model
    campaign = relationship("Campaign", back_populates="users")

# Example Campaign model
class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    token_id = Column(String, unique=True)

    # Relationship to the User model
    users = relationship("User", back_populates="campaign")

# Create the tables in the database
Base.metadata.create_all(bind=engine)
