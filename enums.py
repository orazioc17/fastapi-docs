from enum import Enum

# By inheriting from str the API docs will be able to know that the values must be of 
# type string and will be able to render correctly.
class ModelName(str, Enum):
    # These are machine learning models names
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Tags(str, Enum):
    """
    Enum for tags of documentation on the url handlers
    """
    first_steps = "First Steps"
    path_parameters = "Path Parameters"
    query_parameters = "Query Parameters"
    request_body = "Request Body"
    validations = "Validations"
