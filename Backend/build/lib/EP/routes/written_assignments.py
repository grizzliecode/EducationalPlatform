from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime

router = APIRouter(tags=['written_assignment'])

@router.post("/assignments/create", status_code=status.HTTP_201_CREATED)
def create_assignment(
    request: schema.AssignmentModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to create an assignment."
        )
    
    # Ensure the class exists
    classroom = db.query(model.Classroom).filter(model.Classroom.id == request.class_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {request.class_id} not found."
        )
    
    # Create the assignment
    new_assignment = model.Assignment(
        description=request.description,
        class_id=request.class_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Assignment created successfully", "assignment": new_assignment}

@router.get("/assignments/{class_id}", status_code=status.HTTP_200_OK)
def get_assignments(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    assignments = db.query(model.Assignment).filter(model.Assignment.class_id == class_id).all()
    if not assignments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No assignments found for class with ID {class_id}."
        )
    return {"assignments": assignments}


@router.get("/assignments/{class_id}/{assignment_id}", status_code=status.HTTP_200_OK)
def get_assignment(
    class_id: int,
    assignment_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    assignment = db.query(model.Assignment).filter(
        model.Assignment.class_id == class_id,
        model.Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with ID {assignment_id} not found in class with ID {class_id}."
        )
    return {"assignment": assignment}


@router.put("/assignments/{class_id}/{assignment_id}", status_code=status.HTTP_200_OK)
def update_assignment(
    class_id: int,
    assignment_id: int,
    request: schema.AssignmentModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to update this assignment."
        )
    
    assignment = db.query(model.Assignment).filter(
        model.Assignment.class_id == class_id,
        model.Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with ID {assignment_id} not found in class with ID {class_id}."
        )
    
    # Update fields
    assignment.description = request.description
    db.commit()
    db.refresh(assignment)
    return {"message": "Assignment updated successfully", "assignment": assignment}


@router.delete("/assignments/{class_id}/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    class_id: int,
    assignment_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to delete this assignment."
        )
    
    assignment = db.query(model.Assignment).filter(
        model.Assignment.class_id == class_id,
        model.Assignment.assignment_id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with ID {assignment_id} not found in class with ID {class_id}."
        )
    
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}
