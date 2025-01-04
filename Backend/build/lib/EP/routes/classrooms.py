from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime


router = APIRouter( tags=['classroom'])


@router.post("/classrooms/create", status_code=status.HTTP_201_CREATED)
def create_classroom(
    request: schema.ClassroomModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to create a classroom."
        )
    
    # Check if the teacher exists and is a teacher
    teacher = db.query(model.User).filter(model.User.id == request.teacher_id, model.User.teacher == True).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {request.teacher_id} is not a valid teacher."
        )
    
    # Create a new classroom
    new_classroom = model.Classroom(
        class_name=request.class_name,
        teacher_id=request.teacher_id
    )
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return {"message": "Classroom created successfully", "classroom": new_classroom}


@router.get("/classrooms", status_code=status.HTTP_200_OK)
def get_all_classrooms(
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    classrooms = db.query(model.Classroom).all()
    return {"classrooms": classrooms}


@router.get("/classrooms/{classroom_id}", status_code=status.HTTP_200_OK)
def get_classroom_by_id(
    classroom_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view this classroom."
        )
    
    classroom = db.query(model.Classroom).filter(model.Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {classroom_id} not found."
        )
    return {"classroom": classroom}


@router.put("/classrooms/{classroom_id}", status_code=status.HTTP_200_OK)
def update_classroom(
    classroom_id: int,
    request: schema.ClassroomModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to update a classroom."
        )
    
    classroom = db.query(model.Classroom).filter(model.Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {classroom_id} not found."
        )
    
    # Validate the new teacher_id if it's being updated
    if request.teacher_id != classroom.teacher_id:
        teacher = db.query(model.User).filter(model.User.id == request.teacher_id, model.User.teacher == True).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {request.teacher_id} is not a valid teacher."
            )
    
    # Update classroom fields
    classroom.class_name = request.class_name
    classroom.teacher_id = request.teacher_id
    db.commit()
    db.refresh(classroom)
    return {"message": "Classroom updated successfully", "classroom": classroom}


@router.delete("/classrooms/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(
    classroom_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to delete a classroom."
        )
    
    classroom = db.query(model.Classroom).filter(model.Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {classroom_id} not found."
        )
    
    db.delete(classroom)
    db.commit()
    return {"message": "Classroom deleted successfully"}
