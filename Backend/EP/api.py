from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import model, schema
from .database import engine
from .routes import classrooms, code_assignments, written_assignments, code_submission, written_submissions, users, authentication, class_students

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:5173",  # Vite development server
    "http://127.0.0.1:5173", # Alternate localhost
    # Add more origins if deploying to other environments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(classrooms.router)
app.include_router(class_students.router)
app.include_router(written_assignments.router)
app.include_router(written_submissions.router)
app.include_router(code_assignments.router)
app.include_router(code_submission.router)

# Create database tables
model.Base.metadata.create_all(engine)

@app.get("/")
def get_hello():
    return {
        "data": "Hello world"
    }
