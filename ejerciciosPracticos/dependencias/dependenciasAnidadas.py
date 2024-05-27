from typing import Annotated
from fastapi import Depends, FastAPI, Header

app = FastAPI()

def getLastname(lastname: Annotated[str, Header()]):
    return lastname

class User:
    def __init__(self, firstname: str, 
                 lastname: Annotated[str, Depends(getLastname)]):
        self.firtsname = firstname
        self.lastname = lastname

    @property
    def fullname(self) -> str:
        return f'{self.firtsname} {self.lastname}'
    
@app.post('/hello')
def hello(user: Annotated[str, Depends(User)]):
    return f'Hello {user.fullname}'

@app.get('/goodbye')
def goodBye(lastname: str = Depends(getLastname)):
    return f'Goodbye {lastname}'