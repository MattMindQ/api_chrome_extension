# File: main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from routes import company_router, project_router, team_router, contact_router, news_router

load_dotenv()

app = FastAPI()

# Use environment variable for the URI
uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
db = client.company_data

# Include routers
app.include_router(company_router, prefix="/api/companies", tags=["companies"])
app.include_router(project_router, prefix="/api/companies", tags=["projects"])
app.include_router(team_router, prefix="/api/companies", tags=["teams"])
app.include_router(contact_router, prefix="/api/companies", tags=["contacts"])
app.include_router(news_router, prefix="/api/companies", tags=["news"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)