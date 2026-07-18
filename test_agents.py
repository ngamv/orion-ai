from core.agent_manager import AgentManager


manager = AgentManager()

agents = manager.load_agents()

print("Agents chargés :")
print(manager.list_agents())