from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routes.health import router as health_router
from app.routes.orchestrator import router as orchestrator_router
from app.routes.memory import router as memory_router
from app.routes.tools import router as tools_router
from app.routes.agents import router as agents_router

app = FastAPI(
    title=settings.APP_NAME,
    description="F.R.I.D.A.Y AI orchestration core for routing prompts, providers, agents, memory, and tools.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(orchestrator_router)
app.include_router(memory_router)
app.include_router(tools_router)
app.include_router(agents_router)


@app.get("/")
def root():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "message": "F.R.I.D.A.Y AI Orchestrator is running",
    }