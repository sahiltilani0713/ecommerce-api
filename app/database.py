# Import the tools we need from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The URL that tells SQLAlchemy where our SQLite database file lives
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

# Create the engine that connects to our database
# check_same_thread=False is needed because SQLite only allows one thread by default
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory — each session is like a conversation with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
Base = declarative_base()


# Dependency that gives a database session to each request and closes it when done
def get_db():
    # Create a new session
    db = SessionLocal()
    try:
        # Give the session to whoever asked for it
        yield db
    finally:
        # Always close the session when the request is finished
        db.close()
