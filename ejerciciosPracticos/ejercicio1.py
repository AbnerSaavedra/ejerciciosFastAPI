from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    nombre: str
    edad: int
    email: str
    password: str
    @field_validator('nombre')
    def name_validations(cls, nombre):
        if len(nombre) == 0 or nombre == "":
            raise ValueError('Debe ingresar el nombre.')
        return nombre
    @field_validator('edad')
    def age_validation(cls, edad):
        if edad < 18:
            raise ValueError('Edad no permitida, menor de edad')
        if edad  > 60:
            raise ValueError('Edad no permitida, persona en edad de jubilación')
    @field_validator('email')
    def email_validation(cls, email):
        try:
            v = validate_email(email)
            email = v['email']
        except EmailNotValidError as e:
            raise ValueError('Email no permitido'. str(e))
    @field_validator('password')
    def password_validation(cls, password):
        if len(password) < 5:
            raise ValueError('La contraseña debe tener al menos 5 caracteres')
        

user = User(nombre="Abner", edad=32, email="email@email.com", password="12345")

print("User: ", user)