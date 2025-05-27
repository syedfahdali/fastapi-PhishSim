from fastapi import FastAPI, Depends, HTTPException
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
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Log email and password in the terminal
        print(f"New user registered - Email: {user.email}, Password: {user.password}")

        # Check if the user already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create the user and store it in the database without hashing the password
        new_user = models.User(email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return success message
        return {"message": "User created successfully", "email": new_user.email , "password":new_user.password}
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error during user registration: {str(e)}")
        
        # Return a JSON response in case of error
        return {"detail": "Internal Server Error", "error": str(e)}

# Serve the index.html file on the base route
@app.get('/')
async def landing_page():
    # Ensure the index.html file is in the same directory as this FastAPI app
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    return FileResponse(html_path)

@app.get('/linkedin')
async def landing_page2():
    # Ensure the index.html file is in the same directory as this FastAPI app
    html_path = os.path.join(os.path.dirname(__file__), 'linkedin.html')
    return FileResponse(html_path)
