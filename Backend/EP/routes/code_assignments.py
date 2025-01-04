from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime

router = APIRouter(tags = ["code_tests"])

@router.post("/coding_tests/create", status_code=status.HTTP_201_CREATED)
def create_coding_test(
    request: schema.CodingTestModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to create a coding test."
        )
    
    # Ensure the class exists
    classroom = db.query(model.Classroom).filter(model.Classroom.id == request.class_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Classroom with ID {request.class_id} not found."
        )
    
    # Create the coding test
    new_coding_test = model.CodingTest(
        class_id=request.class_id,
        language=request.language,
        input_file=request.input_file,
        output_file=request.output_file,
        description=request.description
    )
    db.add(new_coding_test)
    db.commit()
    db.refresh(new_coding_test)
    return {"message": "Coding test created successfully", "coding_test": new_coding_test}


@router.get("/coding_tests/{class_id}", status_code=status.HTTP_200_OK)
def get_coding_tests(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view coding tests."
        )
    
    coding_tests = db.query(model.CodingTest).filter(model.CodingTest.class_id == class_id).all()
    if not coding_tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No coding tests found for class with ID {class_id}."
        )
    return {"coding_tests": coding_tests}


@router.get("/coding_tests/{class_id}/{test_id}", status_code=status.HTTP_200_OK)
def get_coding_test(
    class_id: int,
    test_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to view this coding test."
        )
    
    coding_test = db.query(model.CodingTest).filter(
        model.CodingTest.class_id == class_id,
        model.CodingTest.test_id == test_id
    ).first()
    if not coding_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {test_id} not found in class with ID {class_id}."
        )
    return {"coding_test": coding_test}


@router.put("/coding_tests/{class_id}/{test_id}", status_code=status.HTTP_200_OK)
def update_coding_test(
    class_id: int,
    test_id: int,
    request: schema.CodingTestModel,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to update this coding test."
        )
    
    coding_test = db.query(model.CodingTest).filter(
        model.CodingTest.class_id == class_id,
        model.CodingTest.test_id == test_id
    ).first()
    if not coding_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {test_id} not found in class with ID {class_id}."
        )
    
    # Update fields
    coding_test.language = request.language
    coding_test.input_file = request.input_file
    coding_test.output_file = request.output_file
    coding_test.description = request.description
    db.commit()
    db.refresh(coding_test)
    return {"message": "Coding test updated successfully", "coding_test": coding_test}



@router.delete("/coding_tests/{class_id}/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coding_test(
    class_id: int,
    test_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    if not current_user.global_admin and not current_user.teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have sufficient privileges to delete this coding test."
        )
    
    coding_test = db.query(model.CodingTest).filter(
        model.CodingTest.class_id == class_id,
        model.CodingTest.test_id == test_id
    ).first()
    if not coding_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {test_id} not found in class with ID {class_id}."
        )
    
    db.delete(coding_test)
    db.commit()
    return {"message": "Coding test deleted successfully"}
