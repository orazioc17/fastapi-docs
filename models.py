from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None  # Declaring it by default
    price: float 
    tax: float | None = None 