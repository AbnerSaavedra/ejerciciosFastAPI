from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from datetime import *

#https://codigofacilito.com/articulos/fechas-python

app = FastAPI()

tiposHabitaciones = ["Individual", "Matrimonial", "Familiar"]

class reservaHotel(BaseModel):
    fechaEntrada: date
    fechaSalida: date
    numeroHuespedes: int
    tipoHabitacion: str
    @field_validator("fechaEntrada", "fechaSalida")
    def validarFechasReservacion(cls, fechaEntrada,fechaSalida):
        if fechaSalida <= fechaEntrada:
            raise ValueError("Fecha de salida no puede ser menor a la de entrada.")
    @field_validator("tipoHabitacion")
    def validarTipoHabitacion(tipoHabitacion):
        if tipoHabitacion in tiposHabitaciones:
            print("Tipo de habitación válido")
        else:
            raise ValueError("Tipo de habitación no válido.")

        
#Sumar dos días a la fecha actual
now = datetime.now()
new_date = now + timedelta(days=2)
print(new_date)

#Comparación
if now < new_date:
    print("La fecha actual es menor que la nueva fecha")


fecha1 = datetime(year=2024, month=5, day=22).date()
fecha2 = datetime(year=2024, month=5, day=20).date()
if fecha1 > fecha2:
    print("Error")
#fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
reserva = reservaHotel(fechaEntrada=fecha1, fechaSalida=fecha2, numeroHuespedes=10, tipoHabitacion="Matrimonial")

print(reserva)

print("Fecha1: ", fecha1, "Fecha 2: ", fecha2)


