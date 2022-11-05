from enum import Enum

from fastapi import FastAPI


# By inheriting from str the API docs will be able to know that the values must be of 
# type string and will be able to render correctly.
class ModelName(str, Enum):
    # These are machine learning models names
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


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


@app.get("/path/parameters/{path_parameter}")
async def using_path_parameter(path_parameter: str):
    return {"path_parameter": path_parameter}


@app.get("/models/{model_name}")
async def get_model(model_name = ModelName):
    # Learning at the same time how to interact with enums in python
    # I was using "is" for the compare but it wasn't working, "==" did
    # "is" started working when I used model_name.alexnet.value
    if model_name is ModelName.alexnet.value:  
        return {"model_name": model_name, "message": "Deep Learning Model!"}
    elif model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}




