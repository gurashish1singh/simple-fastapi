from typing import Any
from typing import Optional

from enum import Enum

from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Annotated


app = FastAPI()

FAKE_ITEMS_DB = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
    {"item_name": "Laz"},
    {"item_name": "Bat"},
    {"item_name": "Ball"},
]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ModelName(str, Enum):
    MODEL_Y = "Model Y"
    MODEL_X = "Model X"


"""
All GET
"""


@app.get("/")
async def root():
    return {"message": "Hello Person. We are doing a fastapi tutorial from scratch."}


# Passing params and type conversion/validation
# @app.get("/items/{item_id}")
# async def read_item(item_id: int) -> dict[str, int]:
#     return {"item_id": item_id}


# Query params
# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return FAKE_ITEMS_DB[skip: skip + limit]


# Order of route and sub-route matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/")
async def read_users_dupe():
    return ["All", "Users"]


@app.get("/users/")
async def read_users():
    return ["One", "User"]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) -> dict[str, str]:
    if model_name == ModelName.MODEL_X:
        return {"model_name": model_name, "message": "This is a meh car"}
    elif model_name == ModelName.MODEL_Y:
        return {"model_name": model_name, "message": "This is also a meh car"}


# Optional params turn into query params
@app.get("/items/{item_id}")
async def read_item(
    item_id: str, q: Optional[str] = None, short: bool = False,
) -> dict[str, str]:
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description": "Testing bool params. This is being added by default. Send in short to suppress."
        })
    return item


# Reading multiple inputs
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Custom validation for query params
# Old format
# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(default=None, min_length=50)) -> dict[str, Any]:
#     item = {
#         "test": "foo",
#         "bar": "custom validation for query params"
#     }
#     if q:
#         item.update({"q": q})
#     return item


# New format with Annotated
# Annotated is new in py3.9 and can be used to pass metadata for arguments
# @app.get("/items/")
# async def read_items(q: Annotated[Optional[str], Query(min_length=50)] = "fixedquery") -> dict[str, Any]:
#     item = {
#         "test": "foo",
#         "bar": "custom validation for query params"
#     }
#     if q:
#         item.update({"q": q})
#     return item


# Lis query params
# @app.get("/items/")
# async def read_items(q: Annotated[Optional[list[str]], Query()] = None) -> dict[str, Any]:
#     item = {
#         "test": "foo",
#         "bar": "custom validation for query params"
#     }
#     if q:
#         item.update({"q": q})
#     return item


# Add Query metadata
@app.get("/items/")
async def read_items(
    q: Annotated[Optional[str], Query(
        title="Some query title",
        min_length=3
    )] = None
) -> dict[str, Any]:
    item = {
        "test": "foo",
        "bar": "custom validation for query params"
    }
    if q:
        item.update({"q": q})
    return item

"""
All POST
"""


# Use pydatic for input validation and parsing when sending a request body
@app.post("/items/")
async def create_item(item: Item) -> dict[str, Any]:
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"total_price": price_with_tax})
    return item_dict


# Path param and request body together
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item) -> dict[str, Any]:
#     return {"item_id": item_id, **item.dict()}


# Query, Path params, and request body together
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None) -> dict[str, Any]:
    item_dict = {"item_id": item_id, **item.dict()}
    if q:
        item_dict.update({"q": q})
    return item_dict
