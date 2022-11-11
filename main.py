from fastapi import FastAPI, Query, Path
from pydantic import Required

from typing import List

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


# Query Parameters and String Validations
@app.get("/read-items/", tags=[Tags.query_parameters, Tags.validations])
async def read_items(
    q: str | None = Query(default=None, min_length=3, max_length=50)):  # We could also use another thing as default and it will still be optional
    # If we don't use default value, it will be REQUIRED
    """
    # Additional validation
    We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters. It's automated by pydantic validations using Query from FastAPI
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    
    return results


@app.get("/read-items-2/", tags=[Tags.query_parameters, Tags.validations])
async def read_items_2(
    q: str = Query(default=..., min_length=3, max_length=50)):  # We could make the query parameter required just by not give it a default value or default=...  
    # ... is called ellipsis in python and is used by FastAPI and Pydantic to explicitly declare that a value is required
    """
    Declaring a query parameter as required with ellipsis
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    
    return results


@app.get("/read-items-3/", tags=[Tags.query_parameters, Tags.validations])
async def read_items_3(
    q: str | None = Query(default=Required, min_length=3, max_length=50)):  # We could even use Pydantic's Required to explicitly requiring a parameter without using ...  
    """
    # Required with None
    You can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None.
    To do that, you can declare that None is a valid type but still use default=...
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    
    return results


@app.get("/read-items-4/", tags=[Tags.query_parameters, Tags.validations])
async def read_items_4(
    q: List[str] | None = Query(
        default=None,
        title="Query string",
        description="This is a query string and I am using more information about the parameter to show on docs"
    )
):
    # We could even define a default list if the query parameter is None, like Query(default=["Foo", "Bar"])
    """
    # Query parameter list / multiple values
    When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in other way, to receive multiple values.

    For example, to declare a query parameter q that can appear multiple times in the URL, you can use what is used in this function
    
    url example: http://localhost:8000/items/?q=foo&q=bar
    It's return: 
    {
        "q": [
            "foo",
            "bar"
        ]
    }
    To declare a query parameter with a type of list, like in the example above, you need to explicitly use Query, otherwise it would be interpreted as a request body.
    """
    query_items = {"q": q}
    
    # This will receive the multiple q query parameter's values in a python list inside the path operation function, in the function parameter q

    return query_items


# Path Parameters and Numeric Validations
# In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.
@app.get("/path-validation/{item_id}", tags=[Tags.path_parameters, Tags.validations])
async def path_validation(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query", title="Tue optional query to get")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/path-validation-2/{item_id}", tags=[Tags.path_parameters, Tags.validations])
async def path_validation_2(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    """
    # Order the parameters as you need, tricks
    If you want to declare the q query parameter without a Query nor any default value, and the path parameter item_id using Path, and have them in a different order, Python has a little special syntax for that.

    Pass *, as the first parameter of the function.

    Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
    
    Otherwise, q would have to be ordered before item_id
    """
    
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
