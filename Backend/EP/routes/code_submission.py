from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime

router = APIRouter(tags=['code_submission'])

@router.post("/code-submissions/create", status_code=status.HTTP_201_CREATED)
def create_code_submission(
    request: schema.StudentCodeSubmissionModel,
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
    
    # Ensure the coding test exists
    coding_test = db.query(model.CodingTest).filter(model.CodingTest.test_id == request.test_id).first()
    if not coding_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {request.test_id} not found."
        )
    
    # Create the code submission
    new_submission = model.StudentCodeSubmission(
        student_id=request.student_id,
        class_id=request.class_id,
        test_id=request.test_id,
        code_file=request.code_file,
        mark=request.mark
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Code submission created successfully", "submission": new_submission}

@router.get("/code-submissions/{class_id}", status_code=status.HTTP_200_OK)
def get_code_submissions(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view code submissions."
        )
    
    submissions = db.query(model.StudentCodeSubmission).filter(model.StudentCodeSubmission.class_id == class_id).all()
    if not submissions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No code submissions found for class with ID {class_id}."
        )
    return {"submissions": submissions}

@router.get("/code-submissions/{class_id}/{student_id}/{test_id}", status_code=status.HTTP_200_OK)
def get_code_submission(
    class_id: int,
    student_id: int,
    test_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    submission = db.query(model.StudentCodeSubmission).filter(
        model.StudentCodeSubmission.class_id == class_id,
        model.StudentCodeSubmission.student_id == student_id,
        model.StudentCodeSubmission.test_id == test_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code submission for student ID {student_id}, class ID {class_id}, and test ID {test_id} not found."
        )
    return {"submission": submission}

@router.put("/code-submissions/{class_id}/{student_id}/{test_id}", status_code=status.HTTP_200_OK)
def update_code_submission(
    class_id: int,
    student_id: int,
    test_id: int,
    request: schema.StudentCodeSubmissionModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    
    submission = db.query(model.StudentCodeSubmission).filter(
        model.StudentCodeSubmission.class_id == class_id,
        model.StudentCodeSubmission.student_id == student_id,
        model.StudentCodeSubmission.test_id == test_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code submission for student ID {student_id}, class ID {class_id}, and test ID {test_id} not found."
        )
    
    # Update fields
    submission.code_file = request.code_file
    submission.mark = request.mark
    db.commit()
    db.refresh(submission)
    return {"message": "Code submission updated successfully", "submission": submission}

@router.delete("/code-submissions/{class_id}/{student_id}/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_code_submission(
    class_id: int,
    student_id: int,
    test_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):

    submission = db.query(model.StudentCodeSubmission).filter(
        model.StudentCodeSubmission.class_id == class_id,
        model.StudentCodeSubmission.student_id == student_id,
        model.StudentCodeSubmission.test_id == test_id
    ).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code submission for student ID {student_id}, class ID {class_id}, and test ID {test_id} not found."
        )
    
    db.delete(submission)
    db.commit()
    return {"message": "Code submission deleted successfully"}
