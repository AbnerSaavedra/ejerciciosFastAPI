from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional

class User(BaseModel):
    user: str = Field(min_length=4, max_length=50)
    password: str
    email: str
    age: Optional[int] = None

    '''@field_validator('user')
    def username_length(cls, user):
        if len(user) < 4:
            raise ValueError('La longitud mínima de usuario es de 4 caracteres.')
        if len(user) > 50:
            raise ValueError('La longitud máxima de usuario es de 50 caracteres.')
        return user'''

user = User(user="Abner", password="1234", email="abnersaavedra777@gmail.com")

user2 = User(user="Abner", password="1234", email="abnersaavedra777@gmail.com", age=2)

print("User: ", user)
print("User2: ", user2)

try:
    user3 = User(user="Abner", password="1234")
except ValidationError as e:
    print(e.json())

try:
    user4 = User(user="Alí", password="1234", email="abnersaavedra777@gmail.com")
except ValidationError as e:
    print(e.json())

try:
    user4 = User(user="israelkamakawiwooleovertherainbowisraelkamakawiwooleovertherainbow", password="1234", email="abnersaavedra777@gmail.com")
except ValidationError as e:
    print(e.json())
