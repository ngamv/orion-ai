"""Gestionnaire des agents ORION"""
import yaml
from pathlib import Path

class AgentManager:
    def __init__(self):
        self.agents = {}
        self._load_agents()

    def _load_agents(self):
        agents_dir = Path("agents")
        for yaml_file in agents_dir.rglob("*.yaml"):
            with open(yaml_file) as f:
                config = yaml.safe_load(f)
                if config:
                    self.agents[config["id"]] = config

    def get_agent(self, agent_id: str) -> dict:
        return self.agents.get(agent_id)

    def list_agents(self) -> list:
        return list(self.agents.values())
