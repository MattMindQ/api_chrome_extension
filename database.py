# File: database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'), ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client.company_data

async def create_or_update_company(company_data):
    result = await db.companies.update_one(
        {"linkedin_id": company_data["linkedin_id"]},
        {"$set": company_data},
        upsert=True
    )
    return result

async def get_company_by_linkedin_id(linkedin_id):
    return await db.companies.find_one({"linkedin_id": linkedin_id})

async def create_or_update_contact(contact_data):
    result = await db.contacts.update_one(
        {"linkedin_id": contact_data["linkedin_id"]},
        {"$set": contact_data},
        upsert=True
    )
    return result

async def get_contact_by_linkedin_id(linkedin_id):
    return await db.contacts.find_one({"linkedin_id": linkedin_id})

# Add similar functions for projects, teams, and news