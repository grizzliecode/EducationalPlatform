from fastapi import FastAPI
from . import model, schema
from .database import engine
from .routes import classrooms, code_assignments, written_assignments, code_submission, written_submissions, users, authentication, class_students


app = FastAPI()
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(classrooms.router)
app.include_router(class_students.router)
app.include_router(written_assignments.router)
app.include_router(written_submissions.router)
app.include_router(code_assignments.router)
app.include_router(code_submission.router)

model.Base.metadata.create_all(engine)

@app.get("/")
def get_hello():
    return {
        "data": "Hello world"
    }