from fastapi import APIRouter, Depends, Response
from datetime import datetime, timedelta, timezone
from .. import schema
from .. import model
from .. import hashing
from .. import database
from .. import token1
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
def login(response:Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    hash_passw = hashing.hash_string(request.password)
    user = db.query(model.User).filter(model.User.gmail == request.username).filter(model.User.hashed_pass == hash_passw).first()
    if not user:
        response.status_code = 404
    else:
        access_token_expires = timedelta(minutes=token1.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = token1.create_access_token(
            data={"sub": user.gmail}, expires_delta=access_token_expires
        )
        return token1.Token(access_token=access_token, token_type="bearer")