from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from .. import schema
from .. import model
from .. import hashing
from .. import database
from sqlalchemy.orm import Session
from .. import oauth2
import datetime
from DockerHelper.FileHandler import save_string_to_file, get_string_from_file, STORAGE
from DockerHelper import DockerHelper, DockerHelperException
import os
from uuid import uuid4
import time


def analyze(input_file, output_file, language, source_code):
    dh = DockerHelper()
    container_path = "/work"
    containerId = dh.createContainer(containerImage="eval-image", command=["tail", "-f", "/dev/null"], volume=None)
    input_name = os.path.basename(input_file)
    output_name = os.path.basename(output_file)
    source_name = os.path.basename(source_code)
    with open(input_file) as fin:
        text = str(fin.read())
        dh.coppyToContainer(containerId=containerId, data_string=text, container_path=container_path, file_name=input_name)
    with open(output_file) as fin:
        text = str(fin.read())
        dh.coppyToContainer(containerId=containerId, data_string=text, container_path=container_path, file_name="coppy_"+output_name)
    with open(source_code) as fin:
        text = str(fin.read())
        dh.coppyToContainer(containerId=containerId, data_string=text, container_path=container_path, file_name=source_name)
    CMD = ["python", "evaluate.py", "-l", language, "-i", os.path.join(container_path, input_name),
            "-o", os.path.join(container_path, "coppy_"+output_name), "-f",os.path.join(container_path, output_name), "-s", os.path.join(container_path,source_name)]
    dh.execCommand(containerId=containerId, command=CMD)
    start_time = time.time()
    file_found = False
    while time.time() - start_time < 5:
        try:
            result = dh.execCommand(containerId=containerId, command=["test", "-f","/work/clues.txt"])
            # Check the exit code (0 means the file exists)
            if result == 0:
                file_found = True
                break
        except DockerHelperException:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Wait before the next check
        time.sleep(0.5)
    if file_found:
        message = dh.coppyFromContainer(container_path="/work/clues.txt", containerId=containerId)
        if message == "Accepted":
            return 10
        elif message =="Wrong Answer":
            return 3
        else:
            return 1
    else:
        return 1


router = APIRouter(tags=['code_submission'])

@router.post("/code-submissions/create", status_code=status.HTTP_201_CREATED)
def create_code_submission(
    student_id: int = Form(...),
    class_id: int = Form(...),
    test_id: int = Form(...),
    code_file:str = Form(...),
    db: Session = Depends(database.get_db),
    source_code: UploadFile = File(...),
    current_user: schema.UserModel = Depends(oauth2.get_current_user)
):  
    # Ensure the class exists
    request = schema.StudentCodeSubmissionModel(student_id=student_id, class_id=class_id, test_id=test_id,code_file=code_file)
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
    source_file_path = os.path.join(STORAGE, f"{uuid4()}/{request.code_file}")
    os.makedirs(os.path.dirname(source_file_path))
    with open(source_file_path, "wb") as f:
        f.write(source_code.file.read())
    mark = analyze(coding_test.input_file,coding_test.output_file,coding_test.language, source_file_path)
    # Create the code submission
    new_submission = model.StudentCodeSubmission(
        student_id=request.student_id,
        class_id=request.class_id,
        test_id=request.test_id,
        code_file=source_file_path,
        mark= mark
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
    return {"submissions": [schema.StudentCodeSubmissionModel(student_id=sub.student_id, class_id = sub.class_id,
                                                              test_id=sub.test_id, code_file=os.path.basename(sub.code_file),
                                                              mark=sub.mark) for sub in submissions]}

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
    sub = submission
    return {"submission": schema.StudentCodeSubmissionModel(student_id=sub.student_id, class_id = sub.class_id,
                                                              test_id=sub.test_id, code_file=os.path.basename(sub.code_file),
                                                              mark=sub.mark)}

@router.put("/code-submissions/{class_id}/{student_id}/{test_id}", status_code=status.HTTP_200_OK)
def update_code_submission(
    class_id: int,
    student_id: int,
    test_id: int,
    source_code: UploadFile = File(...),
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
    coding_test = db.query(model.CodingTest).filter(model.CodingTest.test_id == test_id).first()
    if not coding_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coding test with ID {test_id} not found."
        )
    
    source_file_path = os.path.join(STORAGE, f"{uuid4()}/{submission.code_file}")
    os.remove(submission.code_file)
    os.rmdir(os.path.dirname(submission.code_file))
    os.makedirs(os.path.dirname(source_file_path))
    with open(source_file_path, "wb") as f:
        f.write(source_code.file.read())
    mark = analyze(coding_test.input_file,coding_test.output_file,coding_test.language, source_file_path)
    # Update fields
    submission.code_file = source_file_path
    submission.mark = mark
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
    os.remove(submission.code_file)
    os.rmdir(os.path.dirname(submission.code_file))
    db.delete(submission)
    db.commit()
    return {"message": "Code submission deleted successfully"}
