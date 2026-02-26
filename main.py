import uvicorn
from fastapi import FastAPI
from api.endpoints import router as api_router
from core.config import Config
from dotenv import load_dotenv

# Load and validate environment configurations
load_dotenv()
Config.validate()

app = FastAPI(
    title="The Lazy QA Agent",
    description="Autonomous workflow integrating Vision models to generate engineering bug reports.",
    version="1.0.0"
)

# Include asynchronous endpoints
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Service health check for Azure App Service monitoring."""
    return {"status": "active", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)