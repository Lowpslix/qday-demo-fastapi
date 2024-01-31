from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from beanie import Document, Link


class Category(Document):
    name: str

    class Settings:
        name = "categories"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "productivity",
            }
        }

    @field_validator("name")
    def category_name_length_validator(cls, v):
        if len(v) < 2:
            raise ValueError("Category name must be at least 3 characters long")
        return v


class Note(Document):
    content: str
    category: Link[Category]
    date: datetime = datetime.now()

    class Settings:
        name = "notes"

    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is a note",
                "category": "productivity",
            }
        }


class UpdateNote(BaseModel):
    content: Optional[str]
