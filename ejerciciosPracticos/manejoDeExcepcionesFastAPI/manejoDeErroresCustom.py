from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content= { "message": f"I'm a teapot! {exc.name} did something wrong..." }
    )

@app.get('/exception/{name}')
async def custom_exception(name: str):
    if name == "pedro":
        raise CustomException(name=name)
    return {"name": name}