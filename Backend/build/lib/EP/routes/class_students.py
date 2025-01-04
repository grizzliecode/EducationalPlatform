from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime


router = APIRouter(tags = ['class_students'])

@router.post("/class_students/create", status_code=status.HTTP_201_CREATED)
def create_class_student(
    request: schema.ClassStudentModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to add a student to a class."
        )
    
    # Ensure the class exists
    classroom = db.query(model.Classroom).filter(model.Classroom.id == request.class_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {request.class_id} not found."
        )
    
    # Ensure the user exists and is not a teacher
    user = db.query(model.User).filter(model.User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {request.user_id} not found."
        )
    if user.teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teachers cannot be enrolled as students in a class."
        )
    
    # Add the student to the class
    new_class_student = model.ClassStudent(
        user_id=request.user_id,
        class_id=request.class_id,
        average_mark= 0
    )
    db.add(new_class_student)
    db.commit()
    db.refresh(new_class_student)
    return {"message": "Student added to class successfully", "class_student": new_class_student}


@router.get("/class_students/{class_id}", status_code=status.HTTP_200_OK)
def get_students_in_class(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view students in this class."
        )
    
    students = db.query(model.ClassStudent).filter(model.ClassStudent.class_id == class_id).all()
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found for class with ID {class_id}."
        )
    return {"students": students}


@router.get("/class_students/{class_id}/{user_id}", status_code=status.HTTP_200_OK)
def get_class_student(
    class_id: int,
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view this enrollment."
        )
    
    class_student = db.query(model.ClassStudent).filter(
        model.ClassStudent.class_id == class_id,
        model.ClassStudent.user_id == user_id
    ).first()
    if not class_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {user_id} is not enrolled in class with ID {class_id}."
        )
    return {"class_student": class_student}


@router.put("/class_students/{class_id}/{user_id}", status_code=status.HTTP_200_OK)
def update_class_student(
    class_id: int,
    user_id: int,
    request: schema.ClassStudentModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to update this enrollment."
        )
    
    class_student = db.query(model.ClassStudent).filter(
        model.ClassStudent.class_id == class_id,
        model.ClassStudent.user_id == user_id
    ).first()
    if not class_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {user_id} is not enrolled in class with ID {class_id}."
        )
    
    # Update fields
    class_student.average_mark = request.average_mark
    db.commit()
    db.refresh(class_student)
    return {"message": "Class student updated successfully", "class_student": class_student}


@router.delete("/class_students/{class_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_student(
    class_id: int,
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to remove a student from this class."
        )
    
    class_student = db.query(model.ClassStudent).filter(
        model.ClassStudent.class_id == class_id,
        model.ClassStudent.user_id == user_id
    ).first()
    if not class_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {user_id} is not enrolled in class with ID {class_id}."
        )
    
    db.delete(class_student)
    db.commit()
    return {"message": "Student removed from class successfully"}
