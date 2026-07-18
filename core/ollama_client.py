"""Client Ollama pour ORION AI"""
import httpx

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:8b"

class OllamaClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.url = OLLAMA_URL

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "")

    async def chat(self, messages: list) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.url}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False}
            )
            return response.json().get("message", {}).get("content", "")
