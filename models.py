from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CompanyModel(BaseModel):
    linkedin_id: str = Field(..., alias="_id")
    name: str
    industry: str
    founded: int
    employees: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={str: str}
    )

class ProjectModel(BaseModel):
    id: str = Field(..., alias="_id")
    company_linkedin_id: str
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={str: str}
    )

class TeamModel(BaseModel):
    id: str = Field(..., alias="_id")
    company_linkedin_id: str
    name: str
    department: str
    size: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={str: str}
    )

class ContactModel(BaseModel):
    linkedin_id: str = Field(..., alias="_id")
    company_linkedin_id: str
    name: str
    position: str
    email: str
    phone: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={str: str}
    )

class NewsModel(BaseModel):
    id: str = Field(..., alias="_id")
    company_linkedin_id: str
    title: str
    content: str
    publish_date: datetime
    source: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={str: str}
    )