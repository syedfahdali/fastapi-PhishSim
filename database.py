from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create the engine to connect to the database
DATABASE_URL = "sqlite:///./test.db"  # Or your actual database URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session local class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
