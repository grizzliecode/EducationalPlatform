from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime
from DockerHelper import DockerHelper
from DockerHelper import FileHandler
import os
from uuid import uuid4
from typing import Literal, Optional

router = APIRouter(tags = ["code_tests"])

@router.post("/coding_tests/create", status_code=status.HTTP_201_CREATED)
def create_coding_test(
    class_id: int = Form(...),
    language: Literal["python", "c/c++", "java"] = Form(...),
    description: str = Form(None),
    input_file: str = Form(...),
    output_file: str = Form(...),
    db: Session = Depends(database.get_db),
    inputF: UploadFile = File(...),
    outputF: UploadFile = File(...),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    request = schema.CodingTestModel(class_id=class_id,language=language,input_file=input_file,output_file=output_file,description=description)
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
    
    input_file_path = os.path.join(FileHandler.STORAGE, f"{uuid4()}/{request.input_file}")
    output_file_path = os.path.join(FileHandler.STORAGE, f"{uuid4()}/{request.output_file}")
    os.makedirs(os.path.dirname(input_file_path))
    os.makedirs(os.path.dirname(output_file_path))
    with open(input_file_path, "wb") as f:
        f.write(inputF.file.read())
    with open(output_file_path, "wb") as f:
        f.write(outputF.file.read())
    # Create the coding test
    new_coding_test = model.CodingTest(
        class_id=request.class_id,
        language=request.language,
        input_file=input_file_path,
        output_file=output_file_path,
        description=request.description
    )
    db.add(new_coding_test)
    db.commit()
    db.refresh(new_coding_test)
    return {"message": "Coding test created successfully", "coding_test": None}


@router.get("/coding_tests/{class_id}", status_code=status.HTTP_200_OK)
def get_coding_tests(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    
    coding_tests = db.query(model.CodingTest).filter(model.CodingTest.class_id == class_id).all()
    if not coding_tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No coding tests found for class with ID {class_id}."
        )
    return {"coding_tests": [schema.CodingTestModel(test_id=cd.test_id,class_id=cd.class_id, language=cd.language, input_file=os.path.basename(cd.input_file), output_file=
                                                    os.path.basename(cd.output_file), description=cd.description) for cd in coding_tests]}


@router.get("/coding_tests/{class_id}/{test_id}", status_code=status.HTTP_200_OK)
def get_coding_test(
    class_id: int,
    test_id: int,
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    # Check if the current user has privileges
    
    cd = db.query(model.CodingTest).filter(
        model.CodingTest.class_id == class_id,
        model.CodingTest.test_id == test_id
    ).first()
    if not cd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {test_id} not found in class with ID {class_id}."
        )
    return {"coding_test": schema.CodingTestModel(test_id=cd.test_id,class_id=cd.class_id, language=cd.language, input_file=os.path.basename(cd.input_file), output_file=
                                                    os.path.basename(cd.output_file), description=cd.description)}


@router.put("/coding_tests/{class_id}/{test_id}", status_code=status.HTTP_200_OK)
def update_coding_test(
    test_id: int ,
    class_id: int ,
    language: Literal["python", "c/c++", "java"] = Form(...),
    description: str = Form(None),
    input_file: str = Form(...),
    output_file: str = Form(...),
    input: Optional[UploadFile] = File(None),
    output: Optional[UploadFile] = File(None),
    db: Session = Depends(database.get_db),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):
    request = schema.CodingTestModel(class_id=class_id,language=language,input_file=input_file,output_file=output_file,description=description)
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
    if input is not None:
        input_file_path = os.path.join(FileHandler.STORAGE, f"{uuid4()}/{request.input_file}")
        os.remove(coding_test.input_file)    
        os.rmdir(os.path.dirname(coding_test.input_file))
        os.makedirs(os.path.dirname(input_file_path))
        with open(input_file_path, "wb") as f:
            f.write(input.file.read())
    else:
        input_file_path = coding_test.input_file
    if output is not None:
        output_file_path = os.path.join(FileHandler.STORAGE, f"{uuid4()}/{request.output_file}")
        os.remove(coding_test.output_file)
        os.rmdir(os.path.dirname(coding_test.output_file))
        os.makedirs(os.path.dirname(output_file_path))
        with open(output_file_path, "wb") as f:
            f.write(output.file.read())
    else:
        output_file_path = coding_test.output_file
    # Update fields
    coding_test.language = request.language
    coding_test.input_file = input_file_path
    coding_test.output_file = output_file_path
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
    os.remove(coding_test.input_file)
    os.rmdir(os.path.dirname(coding_test.input_file))
    os.remove(coding_test.output_file)
    os.rmdir(os.path.dirname(coding_test.output_file))
    db.delete(coding_test)
    db.commit()
    return {"message": "Coding test deleted successfully"}
