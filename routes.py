from fastapi import APIRouter, HTTPException, Request
from models import CompanyModel, ProjectModel, TeamModel, ContactModel, NewsModel
from loguru import logger

# Configure loguru
logger.add("api.log", rotation="500 MB", level="INFO")

company_router = APIRouter()
project_router = APIRouter()
team_router = APIRouter()
contact_router = APIRouter()
news_router = APIRouter()

def log_exception(e: Exception, operation: str):
    logger.exception(f"Error in {operation}: {str(e)}")

@company_router.post("", response_model=CompanyModel)
async def create_or_update_company(company: CompanyModel, request: Request):
    try:
        result = await request.app.state.db.companies.update_one(
            {"_id": company.linkedin_id},
            {"$set": company.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            logger.info(f"Company created/updated: {company.linkedin_id}")
            return CompanyModel.model_validate(await request.app.state.db.companies.find_one({"_id": company.linkedin_id}))
        else:
            logger.warning(f"Failed to create/update company: {company.linkedin_id}")
            raise HTTPException(status_code=400, detail="Failed to create or update company")
    except Exception as e:
        log_exception(e, "create_or_update_company")
        raise HTTPException(status_code=500, detail="Internal server error")

@company_router.get("/{linkedin_id}", response_model=CompanyModel)
async def get_company(linkedin_id: str, request: Request):
    try:
        company = await request.app.state.db.companies.find_one({"_id": linkedin_id})
        if company:
            logger.info(f"Company retrieved: {linkedin_id}")
            return CompanyModel.model_validate(company)
        logger.warning(f"Company not found: {linkedin_id}")
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as e:
        log_exception(e, "get_company")
        raise HTTPException(status_code=500, detail="Internal server error")

@contact_router.post("", response_model=ContactModel)
async def create_or_update_contact(contact: ContactModel, request: Request):
    try:
        result = await request.app.state.db.contacts.update_one(
            {"_id": contact.linkedin_id},
            {"$set": contact.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            logger.info(f"Contact created/updated: {contact.linkedin_id}")
            return ContactModel.model_validate(await request.app.state.db.contacts.find_one({"_id": contact.linkedin_id}))
        else:
            logger.warning(f"Failed to create/update contact: {contact.linkedin_id}")
            raise HTTPException(status_code=400, detail="Failed to create or update contact")
    except Exception as e:
        log_exception(e, "create_or_update_contact")
        raise HTTPException(status_code=500, detail="Internal server error")

@contact_router.get("/{linkedin_id}", response_model=ContactModel)
async def get_contact(linkedin_id: str, request: Request):
    try:
        contact = await request.app.state.db.contacts.find_one({"_id": linkedin_id})
        if contact:
            logger.info(f"Contact retrieved: {linkedin_id}")
            return ContactModel.model_validate(contact)
        logger.warning(f"Contact not found: {linkedin_id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    except Exception as e:
        log_exception(e, "get_contact")
        raise HTTPException(status_code=500, detail="Internal server error")

@project_router.post("", response_model=ProjectModel)
async def create_or_update_project(project: ProjectModel, request: Request):
    try:
        result = await request.app.state.db.projects.update_one(
            {"_id": project.id},
            {"$set": project.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            logger.info(f"Project created/updated: {project.id}")
            return ProjectModel.model_validate(await request.app.state.db.projects.find_one({"_id": project.id}))
        else:
            logger.warning(f"Failed to create/update project: {project.id}")
            raise HTTPException(status_code=400, detail="Failed to create or update project")
    except Exception as e:
        log_exception(e, "create_or_update_project")
        raise HTTPException(status_code=500, detail="Internal server error")

@project_router.get("/{project_id}", response_model=ProjectModel)
async def get_project(project_id: str, request: Request):
    try:
        project = await request.app.state.db.projects.find_one({"_id": project_id})
        if project:
            logger.info(f"Project retrieved: {project_id}")
            return ProjectModel.model_validate(project)
        logger.warning(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        log_exception(e, "get_project")
        raise HTTPException(status_code=500, detail="Internal server error")

@team_router.post("", response_model=TeamModel)
async def create_or_update_team(team: TeamModel, request: Request):
    try:
        result = await request.app.state.db.teams.update_one(
            {"_id": team.id},
            {"$set": team.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            logger.info(f"Team created/updated: {team.id}")
            return TeamModel.model_validate(await request.app.state.db.teams.find_one({"_id": team.id}))
        else:
            logger.warning(f"Failed to create/update team: {team.id}")
            raise HTTPException(status_code=400, detail="Failed to create or update team")
    except Exception as e:
        log_exception(e, "create_or_update_team")
        raise HTTPException(status_code=500, detail="Internal server error")

@team_router.get("/{team_id}", response_model=TeamModel)
async def get_team(team_id: str, request: Request):
    try:
        team = await request.app.state.db.teams.find_one({"_id": team_id})
        if team:
            logger.info(f"Team retrieved: {team_id}")
            return TeamModel.model_validate(team)
        logger.warning(f"Team not found: {team_id}")
        raise HTTPException(status_code=404, detail="Team not found")
    except Exception as e:
        log_exception(e, "get_team")
        raise HTTPException(status_code=500, detail="Internal server error")

@news_router.post("", response_model=NewsModel)
async def create_or_update_news(news: NewsModel, request: Request):
    try:
        result = await request.app.state.db.news.update_one(
            {"_id": news.id},
            {"$set": news.model_dump(by_alias=True, exclude={"id"})},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            logger.info(f"News created/updated: {news.id}")
            return NewsModel.model_validate(await request.app.state.db.news.find_one({"_id": news.id}))
        else:
            logger.warning(f"Failed to create/update news: {news.id}")
            raise HTTPException(status_code=400, detail="Failed to create or update news")
    except Exception as e:
        log_exception(e, "create_or_update_news")
        raise HTTPException(status_code=500, detail="Internal server error")

@news_router.get("/{news_id}", response_model=NewsModel)
async def get_news(news_id: str, request: Request):
    try:
        news = await request.app.state.db.news.find_one({"_id": news_id})
        if news:
            logger.info(f"News retrieved: {news_id}")
            return NewsModel.model_validate(news)
        logger.warning(f"News not found: {news_id}")
        raise HTTPException(status_code=404, detail="News not found")
    except Exception as e:
        log_exception(e, "get_news")
        raise HTTPException(status_code=500, detail="Internal server error")