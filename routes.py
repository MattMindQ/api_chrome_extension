# File: routes.py
from fastapi import APIRouter, HTTPException
from models import CompanyModel, ProjectModel, TeamModel, ContactModel, NewsModel
import database

company_router = APIRouter()
project_router = APIRouter()
team_router = APIRouter()
contact_router = APIRouter()
news_router = APIRouter()

@company_router.post("", response_model=CompanyModel)
async def create_or_update_company(company: CompanyModel):
    result = await database.create_or_update_company(company.dict(by_alias=True))
    if result.upserted_id:
        return CompanyModel(**await database.get_company_by_linkedin_id(company.linkedin_id))
    elif result.modified_count:
        return CompanyModel(**await database.get_company_by_linkedin_id(company.linkedin_id))
    else:
        raise HTTPException(status_code=400, detail="Failed to create or update company")

@company_router.get("/{linkedin_id}", response_model=CompanyModel)
async def get_company(linkedin_id: str):
    company = await database.get_company_by_linkedin_id(linkedin_id)
    if company:
        return CompanyModel(**company)
    raise HTTPException(status_code=404, detail="Company not found")

@contact_router.post("/{company_linkedin_id}/contacts", response_model=ContactModel)
async def create_or_update_contact(company_linkedin_id: str, contact: ContactModel):
    contact.company_linkedin_id = company_linkedin_id
    result = await database.create_or_update_contact(contact.dict(by_alias=True))
    if result.upserted_id or result.modified_count:
        return ContactModel(**await database.get_contact_by_linkedin_id(contact.linkedin_id))
    else:
        raise HTTPException(status_code=400, detail="Failed to create or update contact")

@contact_router.get("/{company_linkedin_id}/contacts/{linkedin_id}", response_model=ContactModel)
async def get_contact(company_linkedin_id: str, linkedin_id: str):
    contact = await database.get_contact_by_linkedin_id(linkedin_id)
    if contact and contact['company_linkedin_id'] == company_linkedin_id:
        return ContactModel(**contact)
    raise HTTPException(status_code=404, detail="Contact not found")