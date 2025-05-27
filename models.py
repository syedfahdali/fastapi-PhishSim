from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Define the Campaign model to map to the 'campaigns' table in the database
class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String, unique=True, index=True)
    token_id = Column(String, unique=True, index=True)
    
    # Define relationship to link to User
    users = relationship("User", back_populates="campaign")

# Define the User model to map to the 'users' table in the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)  # Foreign key to link to the campaign, nullable=True

    # Define the relationship to the Campaign
    campaign = relationship("Campaign", back_populates="users")
