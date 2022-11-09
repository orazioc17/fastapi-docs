from fastapi import FastAPI

from enums import ModelName, Tags
from models import Item


app = FastAPI()  # Lanzar la app con el comando: uvicorn main:app --reload

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/", tags=[Tags.first_steps.value])
async def root():

    return {"message": "Hello world"}


@app.get("/hola", tags=[Tags.first_steps.value])
async def hola():
    return {"message": "Estas en el endpoint 'hola'"}


@app.get("/testing/int", tags=[Tags.first_steps.value])
async def testing_int():
    return 3


@app.get("/testing/str", tags=[Tags.first_steps.value])
async def testing_str():
    return "testing"


@app.get("/path/parameters/{path_parameter}", tags=[Tags.path_parameters.value])
async def using_path_parameter(path_parameter: str):
    return {"path_parameter": path_parameter}


@app.get("/models/{model_name}", tags=[Tags.path_parameters.value])
async def get_model(model_name = ModelName):
    # Learning at the same time how to interact with enums in python
    # I was using "is" for the compare but it wasn't working, "==" did
    # "is" started working when I used model_name.alexnet.value
    if model_name is ModelName.alexnet.value:  
        return {"model_name": model_name, "message": "Deep Learning Model!"}
    elif model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


# Usyng query parameters
@app.get("/items/", tags=[Tags.query_parameters.value])
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}", tags=[Tags.query_parameters.value])
async def optional_query(item_id: str, q: str | None = None):
    """
    Here I get the required item_id and i get an optional query parameter named "q"
    """
    if q:
        return {"item_id": int(item_id), "q": q}
    else: 
        return {"item_id": item_id}


# Query parameter type converter
@app.get("/another/items/{item_id}", tags=[Tags.query_parameters.value])
async def type_converter(item_id: str, q: str | None = None, short: bool = False):
    """
    Here a bool type will be converted by FastApi

    In this case, if you go to one of the following url:
    * http://127.0.0.1:8000/items/foo?short=1
    * http://127.0.0.1:8000/items/foo?short=True
    * http://127.0.0.1:8000/items/foo?short=true
    * http://127.0.0.1:8000/items/foo?short=on
    * http://127.0.0.1:8000/items/foo?short=yes
    
    Or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.
    """

    item = { "item_id": item_id }
    if q:
        item.update({ "q": q })
    if not short: 
        item.update({ "description": "This is an amazing item that has a long description" })
    
    return item


@app.get("/required/query/parameter", tags=[Tags.query_parameters])

async def required_query_parameters(needy: str):
    """
    Requiring a query parameter, to do that, we just don't add a default value to the query parameter
    """    
    return { "needy": needy }


# Request body section
@app.post("/items", tags=[Tags.request_body])
async def create_item(item: Item): # We have to include the request body the same way we declared path and query parameters
    """
    With just that Python type declaration (Item), FastAPI will:

    * Read the body of the request as JSON.
    * Convert the corresponding types (if needed).
    * Validate the data.
    * If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
    * Give you the received data in the parameter item.
    * As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
    * Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
    * Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
    """
    
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tag": price_with_tax})
    
    return item_dict
