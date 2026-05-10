from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="F.R.I.D.A.Y AI Orchestrator",
    description="AI orchestration service for routing prompts, agents, tools, and memory.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "success": True,
        "service": "F.R.I.D.A.Y AI Orchestrator",
        "message": "AI orchestrator is running"
    }

@app.get("/health")
def health():
    return {
        "success": True,
        "service": "F.R.I.D.A.Y AI Orchestrator",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/orchestrate")
def orchestrate(payload: dict):
    user_message = payload.get("message", "")

    return {
        "success": True,
        "input": user_message,
        "response": f"F.R.I.D.A.Y AI Orchestrator received: {user_message}",
        "agent": "coordinator-agent",
        "timestamp": datetime.utcnow().isoformat()
    }