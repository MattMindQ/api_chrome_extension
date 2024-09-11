# File: models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class CompanyModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    linkedin_id: str
    name: str
    industry: str
    founded: int
    employees: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProjectModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    company_linkedin_id: str
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TeamModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    company_linkedin_id: str
    name: str
    department: str
    size: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ContactModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    linkedin_id: str
    company_linkedin_id: str
    name: str
    position: str
    email: str
    phone: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NewsModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    company_linkedin_id: str
    title: str
    content: str
    publish_date: datetime
    source: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}