"""Orchestrateur ORION AI"""
import httpx
import yaml
import logging
from pathlib import Path
from core.memory import Memory
from core.task_router import TaskRouter

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:3b"

COLLABORATION_RULES = {
    "startup": ["finance", "writer"],
    "saas": ["finance", "writer"],
    "application": ["backend_dev", "frontend_dev"],
    "appli": ["backend_dev", "frontend_dev"],
    "campagne": ["marketing_lead", "writer"],
    "lancement": ["marketing_lead", "writer"],
    "site": ["frontend_dev", "seo_lead"],
    "projet": ["backend_dev", "marketing_lead"],
}

def load_agent_prompt(agent_id: str) -> str:
    for yaml_file in Path("agents").rglob(f"{agent_id}.yaml"):
        with open(yaml_file, encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
                return config.get("system_prompt", f"Tu es {agent_id}, expert dans ORION AI.")
            except:
                pass
    return f"Tu es {agent_id}, expert dans ORION AI."

class Orchestrator:
    def __init__(self):
        self.memory = Memory()
        self.router = TaskRouter()
        self.prompts_cache = {}

    def get_prompt(self, agent_id: str) -> str:
        if agent_id not in self.prompts_cache:
            self.prompts_cache[agent_id] = load_agent_prompt(agent_id)
        return self.prompts_cache[agent_id]

    def detect_collaboration(self, message: str) -> list:
        message_lower = message.lower()
        for keyword, agents in COLLABORATION_RULES.items():
            if keyword in message_lower:
                return agents
        return []

    async def ask_ollama(self, messages: list) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": MODEL, "messages": messages, "stream": False}
            )
            return response.json().get("message", {}).get("content", "")

    async def ask_agent(self, agent_id: str, message: str) -> str:
        history = self.memory.recall(f"history_{agent_id}") or []
        system_prompt = self.get_prompt(agent_id)
        messages = [
            {"role": "system", "content": system_prompt + "\nReponds TOUJOURS en francais. Max 100 mots."},
        ] + history[-4:] + [
            {"role": "user", "content": f"[Reponds en francais, max 100 mots] {message}"}
        ]
        reply = await self.ask_ollama(messages)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        if len(history) > 20:
            history = history[-20:]
        self.memory.remember(f"history_{agent_id}", history, permanent=True)
        return reply

    async def dispatch(self, message: str, agent_id: str = None) -> dict:
        collab_agents = self.detect_collaboration(message)

        if collab_agents and not agent_id:
            agents_str = ", ".join(collab_agents)
            summary_prompt = f"L'utilisateur demande: '{message}'. Tu coordonnes ces experts: {agents_str}. Donne une reponse structuree en sections, une par expert, en francais, max 200 mots."
            messages = [
                {"role": "system", "content": "Tu es Orion, coordinateur d'ORION AI. Reponds TOUJOURS en francais."},
                {"role": "user", "content": summary_prompt}
            ]
            reply = await self.ask_ollama(messages)
            return {
                "agent": "orion",
                "response": f"Collaboration - {agents_str}\n\n{reply}",
                "routed_by": "collaboration",
                "agents_involved": collab_agents
            }

        routed = False
        if not agent_id:
            agent_id = self.router.route(message)
            routed = True

        reply = await self.ask_agent(agent_id, message)

        return {
            "agent": agent_id,
            "response": reply,
            "routed_by": "auto" if routed else "manual"
        }