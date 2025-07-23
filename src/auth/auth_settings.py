from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

annotation_oauth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
token_annotation = Annotated[str, Depends(oauth2_bearer)]
