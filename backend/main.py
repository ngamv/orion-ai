from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
sys.path.append(".")
from core.orchestrator import Orchestrator

app = FastAPI(title="ORION AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
orchestrator = Orchestrator()

from typing import Optional

class ChatRequest(BaseModel):
    message: str
    agent: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "ORION AI is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/agents")
async def list_agents():
    return {"agents": [
        {"id": "orion", "name": "Orion", "team": "CIO", "emoji": "👔"},
        {"id": "researcher", "name": "Researcher", "team": "CIO", "emoji": "🔬"},
        {"id": "writer", "name": "Writer", "team": "CIO", "emoji": "📝"},
        {"id": "finance", "name": "Finance", "team": "CIO", "emoji": "💰"},
        {"id": "backend_dev", "name": "BackendDev", "team": "Dev", "emoji": "💻"},
        {"id": "frontend_dev", "name": "FrontendDev", "team": "Dev", "emoji": "🎨"},
        {"id": "seo_lead", "name": "SEOLead", "team": "SEO", "emoji": "🔍"},
        {"id": "marketing_lead", "name": "Marketing", "team": "Marketing", "emoji": "📈"},
        {"id": "social_lead", "name": "Social", "team": "Social", "emoji": "📱"},
        {"id": "qa_lead", "name": "QALead", "team": "QA", "emoji": "🧪"},
        {"id": "devops_lead", "name": "DevOps", "team": "DevOps", "emoji": "☁️"},
        {"id": "security_lead", "name": "Security", "team": "Securite", "emoji": "🔒"},
    ]}

@app.get("/memory")
async def memory_status():
    return orchestrator.memory.summary()

@app.post("/chat")
async def chat(request: ChatRequest):
    return await orchestrator.dispatch(message=request.message, agent_id=request.agent)

@app.delete("/memory/{agent_id}")
async def clear_memory(agent_id: str):
    orchestrator.memory.forget(f"history_{agent_id}")
    return {"status": "cleared"}
@app.get("/dashboard")
async def dashboard():
    memory_data = orchestrator.memory.summary()
    agents_list = [
        {"id": "orion", "name": "Orion", "team": "CIO", "emoji": "👔"},
        {"id": "researcher", "name": "Researcher", "team": "CIO", "emoji": "🔬"},
        {"id": "writer", "name": "Writer", "team": "CIO", "emoji": "📝"},
        {"id": "finance", "name": "Finance", "team": "CIO", "emoji": "💰"},
        {"id": "backend_dev", "name": "BackendDev", "team": "Dev", "emoji": "💻"},
        {"id": "frontend_dev", "name": "FrontendDev", "team": "Dev", "emoji": "🎨"},
        {"id": "seo_lead", "name": "SEOLead", "team": "SEO", "emoji": "🔍"},
        {"id": "marketing_lead", "name": "Marketing", "team": "Marketing", "emoji": "📈"},
        {"id": "social_lead", "name": "Social", "team": "Social", "emoji": "📱"},
        {"id": "qa_lead", "name": "QALead", "team": "QA", "emoji": "🧪"},
        {"id": "devops_lead", "name": "DevOps", "team": "DevOps", "emoji": "☁️"},
        {"id": "security_lead", "name": "Security", "team": "Securite", "emoji": "🔒"},
    ]
    agents_stats = []
    for agent in agents_list:
        events = orchestrator.memory.get_events(agent["id"])
        history = orchestrator.memory.recall(f"history_{agent['id']}") or []
        agents_stats.append({
            **agent,
            "messages_count": len(history) // 2,
            "events_count": len(events),
            "last_active": events[-1]["timestamp"] if events else None,
            "active": len(history) > 0
        })
    return {
        "memory": memory_data,
        "agents": agents_stats,
        "total_agents": len(agents_list),
        "active_agents": len([a for a in agents_stats if a["active"]]),
        "total_messages": sum(a["messages_count"] for a in agents_stats),
    }