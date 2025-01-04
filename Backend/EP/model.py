from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_pass = Column(String, nullable=False)
    gmail = Column(String, nullable=False)
    global_admin = Column(Boolean, default=False)
    teacher = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    teacher = relationship("User", backref="classes")



class ClassStudent(Base):
    __tablename__ = 'class_student'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("classroom.id"), primary_key=True)
    average_mark = Column(Float)
    student = relationship("User", backref="enrollments")
    classroom = relationship("Classroom", backref="students")


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Assignment(Base):
    __tablename__ = 'assignments'
    assignment_id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classroom.id"))
    classroom = relationship("Classroom", backref="assignments")

class CodingTest(Base):
    __tablename__ = 'coding_test'
    test_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classroom.id"))
    language = Column(String, nullable=False)
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=False)
    description = Column(String)
    classroom = relationship("Classroom", backref="coding_tests")


class StudentAssignmentSubmission(Base):
    __tablename__ = 'student_assignment_submission'
    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("classroom.id"), primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"))
    response_file = Column(String, nullable=False)
    grade = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    student = relationship("User", backref="assignment_submissions")
    classroom = relationship("Classroom", backref="assignment_submissions")
    assignment = relationship("Assignment", backref="submissions")


class StudentCodeSubmission(Base):
    __tablename__ = 'student_code_submission'
    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("classroom.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("coding_test.test_id"))
    code_file = Column(String, nullable=False)
    mark = Column(Integer)
    student = relationship("User", backref="code_submissions")
    classroom = relationship("Classroom", backref="code_submissions")
    coding_test = relationship("CodingTest", backref="submissions")
