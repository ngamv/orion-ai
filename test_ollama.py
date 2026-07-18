from core.ollama_client import OllamaClient


ia = OllamaClient()

reponse = ia.ask(
    "Tu es Orion, le CIO d'un système multi-agents. Présente-toi en français."
)

print(reponse)