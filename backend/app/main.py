import os
import sys
from pathlib import Path
import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from backend/.env for local and deployed runs
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import engine
from app.models import Base
from app.auth import router as auth_router
from app.routes.team import router as team_router
from app.routes.task import router as task_router
from app.routes.dashboard import router as dashboard_router

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

PROJECT_NAME = os.getenv("PROJECT_NAME", "Team Task Manager API")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")] if ALLOWED_ORIGINS else ["*"]

app = FastAPI(title=PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Keep unexpected tracebacks visible in Railway/local logs without leaking them.
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

app.include_router(auth_router)
app.include_router(team_router)
app.include_router(task_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
