from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dummy_users_db = {
   "johndoe": {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "full_name": "John Doe",
    "disabled": False
   },
   "alice": {
    "username": "alice",
    "email": "alice@example.com",
    "full_name": "Alice Wonderson",
    "disabled": True
   } 
}

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

def dumb_decode_token(token):
    return User(username=token + "dummydecoded", email="john@example.com", full_name="John Doe")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = dumb_decode_token(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_user_active(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.disabled:
        raise HTTPException(
            status_code= 400,
            detail="Invalid user"
        )
    return current_user

def dumb_hash_password(password: str):
    return "dumbhashed" + password

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = dummy_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = dumb_hash_password(form_data.password)
    print("hashed_password", hashed_password)
    print("user.hashed_password", user.hashed_password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

