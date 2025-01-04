from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime

router = APIRouter(tags=['written_submission'])

@router.post("/assignment-submissions/create", status_code=status.HTTP_201_CREATED)
def create_assignment_submission(
    request: schema.StudentAssignmentSubmissionModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    # Ensure the class exists
    classroom = db.query(model.Classroom).filter(model.Classroom.id == request.class_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {request.class_id} not found."
        )
    
    # Ensure the student exists
    student = db.query(model.User).filter(model.User.id == request.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {request.student_id} not found."
        )
    
    # Ensure the assignment exists
    assignment = db.query(model.Assignment).filter(model.Assignment.assignment_id == request.assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with ID {request.assignment_id} not found."
        )
    
    # Create the assignment submission
    new_submission = model.StudentAssignmentSubmission(
        student_id=request.student_id,
        class_id=request.class_id,
        assignment_id=request.assignment_id,
        response_file=request.response_file,
        grade=request.grade
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Assignment submission created successfully", "submission": new_submission}
 
@router.get("/assignment-submissions/{class_id}", status_code=status.HTTP_200_OK)
def get_assignment_submissions(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view assignment submissions."
        )
    
    submissions = db.query(model.StudentAssignmentSubmission).filter(model.StudentAssignmentSubmission.class_id == class_id).all()
    if not submissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No assignment submissions found for class with ID {class_id}."
        )
    return {"submissions": submissions}

@router.get("/assignment-submissions/{class_id}/{student_id}/{assignment_id}", status_code=status.HTTP_200_OK)
def get_assignment_submission(
    class_id: int,
    student_id: int,
    assignment_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    submission = db.query(model.StudentAssignmentSubmission).filter(
        model.StudentAssignmentSubmission.class_id == class_id,
        model.StudentAssignmentSubmission.student_id == student_id,
        model.StudentAssignmentSubmission.assignment_id == assignment_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment submission for student ID {student_id}, class ID {class_id}, and assignment ID {assignment_id} not found."
        )
    return {"submission": submission}


@router.put("/assignment-submissions/{class_id}/{student_id}/{assignment_id}", status_code=status.HTTP_200_OK)
def update_assignment_submission(
    class_id: int,
    student_id: int,
    assignment_id: int,
    request: schema.StudentAssignmentSubmissionModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    submission = db.query(model.StudentAssignmentSubmission).filter(
        model.StudentAssignmentSubmission.class_id == class_id,
        model.StudentAssignmentSubmission.student_id == student_id,
        model.StudentAssignmentSubmission.assignment_id == assignment_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment submission for student ID {student_id}, class ID {class_id}, and assignment ID {assignment_id} not found."
        )
    
    # Update the submission fields
    submission.response_file = request.response_file
    submission.grade = request.grade
    db.commit()
    db.refresh(submission)
    return {"message": "Assignment submission updated successfully", "submission": submission}


@router.delete("/assignment-submissions/{class_id}/{student_id}/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment_submission(
    class_id: int,
    student_id: int,
    assignment_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):

    
    submission = db.query(model.StudentAssignmentSubmission).filter(
        model.StudentAssignmentSubmission.class_id == class_id,
        model.StudentAssignmentSubmission.student_id == student_id,
        model.StudentAssignmentSubmission.assignment_id == assignment_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment submission for student ID {student_id}, class ID {class_id}, and assignment ID {assignment_id} not found."
        )
    
    db.delete(submission)
    db.commit()
    return {"message": "Assignment submission deleted successfully"}

