from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import models

# Function to print all users in the database
def print_all_users(db: Session):
    # Query all records in the 'users' table
    users = db.query(models.User).all()

    # Print each user record
    if users:
        print("Users in the database:")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Password: {user.password}")
    else:
        print("No users found in the database.")

# Main function to test the print_all_users function
def main():
    # Open a session to the database
    db = SessionLocal()
    
    # Print all users
    print_all_users(db)
    
    # Close the session
    db.close()

# Run the script
if __name__ == "__main__":
    main()
