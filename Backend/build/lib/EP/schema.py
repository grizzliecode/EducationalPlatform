from pydantic import BaseModel
from typing import List, Optional, Literal
from fastapi import Form

class UserModel(BaseModel):
    user_id : Optional[int] = None
    username: str
    password: str
    gmail: str
    global_admin: bool
    teacher: bool



class ClassroomModel(BaseModel):
    id: Optional[int] =  None
    class_name: str
    teacher_id: int




class ClassStudentModel(BaseModel):
    user_id: int
    class_id: int
    average_mark: Optional[float] = None


class AssignmentModel(BaseModel):
    assignment_id: Optional[int] = None
    description: str
    class_id: int


class CodingTestModel(BaseModel):
    test_id: Optional[int] = None
    class_id: int
    language: Literal["python","c/c++", "java"]
    input_file: str
    output_file: str
    description: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        class_id: int = Form(...),
        language: Literal["python","c/c++", "java"]= Form(...),
        input_file: str= Form(...),
        output_file: str= Form(...),
        test_id: Optional[int] = Form(None),
        description: Optional[str] = Form(None)
    ):
        return cls(class_id=class_id,language=language,input_file=input_file,output_file=output_file,test_id=test_id,description=description)



class StudentAssignmentSubmissionModel(BaseModel):
    student_id: int
    class_id: int
    assignment_id: int
    response_file: str
    grade: Optional[float] = None


class StudentCodeSubmissionModel(BaseModel):
    student_id: int
    class_id: int
    test_id: int
    code_file: str
    mark: Optional[int] = None


class LoginModel(BaseModel):
    gmail : str
    password: str