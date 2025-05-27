from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, get_db
import models
from starlette.responses import FileResponse
import os

# Create the tables in the database (if not already created)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for user input (for registration)
class UserCreate(BaseModel):
    email: str
    password: str

# Create a new user endpoint (Registration)
@app.post("/register/")
async def register_user(
    user: UserCreate, 
    db: Session = Depends(get_db), 
    campaign_id: str = Query(None),  # campaign_id from query parameters
    token: str = Query(None)  # token from query parameters
):
    try:
        # Log email and password in the terminal
        print(f"New user registered - Email: {user.email}, Password: {user.password}")
        print(f"Campaign ID: {campaign_id}, Token: {token}")  # For debugging purposes

        # Check if the user already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # If campaign_id and token are provided, check if the campaign exists in the database
        if campaign_id and token:
            campaign = db.query(models.Campaign).filter(models.Campaign.campaign_id == campaign_id, models.Campaign.token_id == token).first()
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign or Token not found")
        else:
            campaign = None  # If no campaign is provided, campaign will be set to None
        
        # Create the user and store it in the database, associating with the campaign if available
        new_user = models.User(email=user.email, password=user.password, campaign=campaign)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return success message
        return {"message": "User created successfully", "email": new_user.email, "password": new_user.password, "campaign_id": campaign_id, "token": token}
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error during user registration: {str(e)}")
        
        # Return a JSON response in case of error
        return {"detail": "Internal Server Error", "error": str(e)}

# Serve the index.html file on the base route
@app.get('/')
async def landing_page():
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    return FileResponse(html_path)

@app.get('/linkedin')
async def landing_page2():
    html_path = os.path.join(os.path.dirname(__file__), 'linkedin.html')
    return FileResponse(html_path)
