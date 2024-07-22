from __future__ import annotations

from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        default=None,
        title="The descrption of the item.",
        max_length=300,
    )
    price: float = Field(
        gt=0,
        description="The price of the item."
    )
    tax: Optional[float] = None
    tags: list[str] = []
    image: Optional[list[Image]] = None


class User(BaseModel):
    username: str
    name: str
