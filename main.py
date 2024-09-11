from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from routes import company_router, project_router, team_router, contact_router, news_router
import uvicorn
from loguru import logger
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Configure loguru
logger.add("api.log", rotation="500 MB", level="INFO")

# MongoDB setup
uri = os.getenv("MONGODB_URI")
if not uri:
    logger.error("MONGODB_URI environment variable is not set")
    raise ValueError("MONGODB_URI environment variable is not set")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting up")
    try:
        client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
        db = client.company_data
        app.state.db = db
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

    yield  # The application runs here

    # Shutdown
    logger.info("Application shutting down")
    app.state.db.client.close()

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(company_router, prefix="/api/companies", tags=["companies"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(team_router, prefix="/api/teams", tags=["teams"])
app.include_router(contact_router, prefix="/api/contacts", tags=["contacts"])
app.include_router(news_router, prefix="/api/news", tags=["news"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"  # This allows connections from all interfaces
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port)