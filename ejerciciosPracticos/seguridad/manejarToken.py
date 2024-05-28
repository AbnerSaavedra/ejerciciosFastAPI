from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

# To get a string like this run
# openssl rand -hex 32

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

dummy_users_db = {
   "johndoe": {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "hashed_password": "dumbhashedsecret",
    "full_name": "John Doe",
    "disabled": False
   },
   "alice": {
    "username": "alice",
    "email": "alice@example.com",
    "hashed_password": "dumbhashedsecret2",
    "full_name": "Alice Wonderson",
    "disabled": True
   }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def dumb_decode_token(token):
    return User(username=token + "dummydecoded", email="john@example.com", full_name="John Doe")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = dumb_decode_token(token)
    credentials_exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(dummy_users_db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

def dumb_hash_password(password: str):
    return "dumbhashed" + password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def autheticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = autheticate_user(dummy_users_db, form_data.username, form_data.password)
    user = dummy_users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token= access_token, token_type= "bearer")


