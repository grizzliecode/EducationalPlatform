from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime


router = APIRouter( tags=['users'])

@router.get("/users")
def get_users(db: Session = Depends(database.get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    return db.query(model.User).all()
@router.post("/users/create", status_code=status.HTTP_200_OK)
def add_user(request: schema.UserModel, db: Session = Depends(database.get_db)):
    hashed = hashing.hash_string(request.password)
    new_user = model.User(username=request.username, hashed_pass=hashed,gmail=request.gmail, global_admin=False, teacher=request.teacher) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "success"

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    if (not current_user.global_admin) and user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with ID {user_id} does not have enough priviledges"
        )
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, request: schema.UserModel, db: Session = Depends(database.get_db), current_user: schema.UserModel = Depends(oauth2.get_current_user)):
    if (not current_user.global_admin) and user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with ID {user_id} does not have enough priviledges"
        )
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    user.username = request.username
    user.hashed_pass = hashing.hash_string(request.password)
    user.gmail = request.gmail
    if current_user.global_admin:
        user.global_admin = request.global_admin
    else:
        user.global_admin = False
    user.teacher = request.teacher
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}
