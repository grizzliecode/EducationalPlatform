from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from . import model



DATABASE_URL = (
   "postgresql://postgres:gado2211@localhost:5432/educational_platform"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def isAdmin(user_id):
    db = get_db()
    user = db.query(model.User).filter(model.User.id == user_id).filter(model.User.global_admin == True).first()
    if user is None:
        return False
    return True

def isTeacher(user_id):
    db = get_db()
    user = db.query(model.User).filter(model.User.id == user_id).filter(model.User.teacher == True).first()
    if user is None:
        return False
    return True