from fastapi import FastAPI

app = FastAPI()  # Lanzar la app con el comando: uvicorn main:app --reload


@app.get("/", tags=["testing"])
async def root():

    return {"message": "Hello world"}


@app.get("/hola", tags=["testing"])
async def hola():
    return {"message": "Estas en el endpoint 'hola'"}


@app.get("/testing/int", tags=["testing"])
async def testing_int():
    return 3


@app.get("/testing/str", tags=["testing"])
async def testing_str():
    return "testing"
