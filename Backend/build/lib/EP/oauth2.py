from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from .token1 import SECRET_KEY, ALGORITHM, TokenData
from . import model, schema, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        gmail: str = payload.get("sub")
        if gmail is None:
            raise credentials_exception
        token_data = TokenData(gmail=gmail)
    except InvalidTokenError:
        raise credentials_exception
    user = next(database.get_db()).query(model.User).filter(model.User.gmail == gmail).first()
    return schema.UserModel(user_id=user.id, username=user.username, password="", gmail=gmail, global_admin=user.global_admin, teacher=user.teacher)
   