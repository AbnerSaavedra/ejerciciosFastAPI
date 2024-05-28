from typing import Union
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def autheticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, )
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user