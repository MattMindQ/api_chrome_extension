from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import os

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.company_data

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
    name: str
    industry: str
    website: str
    foundedDate: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProjectModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    companyId: PyObjectId
    name: str
    description: str
    startDate: datetime
    endDate: Optional[datetime]
    technologies: List[str]
    status: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TeamModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    companyId: PyObjectId
    name: str
    department: str
    size: int
    responsibilities: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ContactModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    companyId: PyObjectId
    name: str
    position: str
    email: str
    phone: Optional[str]
    socialMedia: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NewsModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    companyId: PyObjectId
    title: str
    content: str
    publishDate: datetime
    source: str
    tags: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@app.post("/api/companies", response_model=CompanyModel)
async def create_company(company: CompanyModel):
    company_dict = company.dict(by_alias=True)
    del company_dict["_id"]
    new_company = await db.companies.insert_one(company_dict)
    created_company = await db.companies.find_one({"_id": new_company.inserted_id})
    return CompanyModel(**created_company)

@app.post("/api/companies/{company_id}/projects", response_model=ProjectModel)
async def create_project(company_id: str, project: ProjectModel):
    project_dict = project.dict(by_alias=True)
    del project_dict["_id"]
    project_dict["companyId"] = ObjectId(company_id)
    new_project = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": new_project.inserted_id})
    return ProjectModel(**created_project)

@app.get("/api/companies/{company_id}/projects", response_model=List[ProjectModel])
async def get_company_projects(company_id: str):
    projects = await db.projects.find({"companyId": ObjectId(company_id)}).to_list(1000)
    return [ProjectModel(**project) for project in projects]

# Implement similar CRUD operations for teams, contacts, and news

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)