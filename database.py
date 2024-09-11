from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from models import CompanyModel, ContactModel, ProjectModel, TeamModel, NewsModel
import logging

load_dotenv()

logger = logging.getLogger(__name__)

uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("MONGODB_URI environment variable is not set")

try:
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    db = client.company_data
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

async def create_or_update_company(company_data: CompanyModel):
    try:
        result = await db.companies.update_one(
            {"_id": company_data.linkedin_id},
            {"$set": company_data.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_or_update_company: {str(e)}")
        raise

async def get_company_by_linkedin_id(linkedin_id: str):
    try:
        return await db.companies.find_one({"_id": linkedin_id})
    except Exception as e:
        logger.error(f"Error in get_company_by_linkedin_id: {str(e)}")
        raise

async def create_or_update_contact(contact_data: ContactModel):
    try:
        result = await db.contacts.update_one(
            {"_id": contact_data.linkedin_id},
            {"$set": contact_data.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_or_update_contact: {str(e)}")
        raise

async def get_contact_by_linkedin_id(linkedin_id: str):
    try:
        return await db.contacts.find_one({"_id": linkedin_id})
    except Exception as e:
        logger.error(f"Error in get_contact_by_linkedin_id: {str(e)}")
        raise

async def create_or_update_project(project_data: ProjectModel):
    try:
        result = await db.projects.update_one(
            {"_id": project_data.id},
            {"$set": project_data.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_or_update_project: {str(e)}")
        raise

async def get_project_by_id(project_id: str):
    try:
        return await db.projects.find_one({"_id": project_id})
    except Exception as e:
        logger.error(f"Error in get_project_by_id: {str(e)}")
        raise

async def create_or_update_team(team_data: TeamModel):
    try:
        result = await db.teams.update_one(
            {"_id": team_data.id},
            {"$set": team_data.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_or_update_team: {str(e)}")
        raise

async def get_team_by_id(team_id: str):
    try:
        return await db.teams.find_one({"_id": team_id})
    except Exception as e:
        logger.error(f"Error in get_team_by_id: {str(e)}")
        raise

async def create_or_update_news(news_data: NewsModel):
    try:
        result = await db.news.update_one(
            {"_id": news_data.id},
            {"$set": news_data.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_or_update_news: {str(e)}")
        raise

async def get_news_by_id(news_id: str):
    try:
        return await db.news.find_one({"_id": news_id})
    except Exception as e:
        logger.error(f"Error in get_news_by_id: {str(e)}")
        raise