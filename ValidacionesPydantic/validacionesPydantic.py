from pydantic import BaseModel, ValidationError
from typing import Optional

class User(BaseModel):
    user: str
    password: str
    email: str
    age: Optional[int] = None

user = User(user="Abner", password="1234", email="abnersaavedra777@gmail.com")

user2 = User(user="Abner", password="1234", email="abnersaavedra777@gmail.com", age=2)

print("User: ", user)
print("User2: ", user2)

try:
    user3 = User(user="Abner", password="1234")
except ValidationError as e:
    print(e.json())
