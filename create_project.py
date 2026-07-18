"""
ORION AI v1.0 - Générateur de projet
Lance ce script depuis la racine de ton projet :
    python create_project.py
"""

import os
import json
import yaml
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION DES 40 AGENTS
# ─────────────────────────────────────────────
AGENTS = {
    "cio": [
        {"id": "orion", "name": "Orion", "role": "Chief Intelligence Officer",
         "description": "Orchestrateur principal. Coordonne tous les agents et prend les décisions stratégiques.",
         "capabilities": ["orchestration", "planning", "decision_making", "reporting"]}
    ],
    "development": [
        {"id": "dev_lead",      "name": "DevLead",      "role": "Lead Developer",         "capabilities": ["architecture", "code_review", "technical_decisions"]},
        {"id": "backend_dev",   "name": "BackendDev",   "role": "Backend Developer",       "capabilities": ["python", "fastapi", "database", "api_design"]},
        {"id": "frontend_dev",  "name": "FrontendDev",  "role": "Frontend Developer",      "capabilities": ["react", "typescript", "css", "components"]},
        {"id": "fullstack_dev", "name": "FullstackDev", "role": "Fullstack Developer",     "capabilities": ["react", "python", "fastapi", "integration"]},
        {"id": "mobile_dev",    "name": "MobileDev",    "role": "Mobile Developer",        "capabilities": ["react_native", "ios", "android"]},
        {"id": "api_dev",       "name": "APIDev",       "role": "API Developer",           "capabilities": ["rest", "graphql", "websocket", "openapi"]},
        {"id": "db_dev",        "name": "DBDev",        "role": "Database Developer",      "capabilities": ["postgresql", "mongodb", "redis", "migrations"]},
        {"id": "ai_dev",        "name": "AIDev",        "role": "AI/ML Developer",         "capabilities": ["llm", "embeddings", "fine_tuning", "rag"]},
        {"id": "integrations",  "name": "Integration",  "role": "Integration Developer",   "capabilities": ["webhooks", "third_party", "automation"]},
        {"id": "code_reviewer", "name": "CodeReviewer", "role": "Code Reviewer",           "capabilities": ["code_quality", "best_practices", "refactoring"]},
    ],
    "uiux": [
        {"id": "ux_designer",  "name": "UXDesigner",  "role": "UX Designer",       "capabilities": ["user_research", "wireframes", "prototypes"]},
        {"id": "ui_designer",  "name": "UIDesigner",  "role": "UI Designer",       "capabilities": ["design_system", "figma", "accessibility"]},
        {"id": "ux_writer",    "name": "UXWriter",    "role": "UX Writer",         "capabilities": ["microcopy", "content_strategy", "onboarding"]},
    ],
    "seo": [
        {"id": "seo_lead",      "name": "SEOLead",      "role": "SEO Lead",          "capabilities": ["strategy", "audits", "reporting"]},
        {"id": "seo_technical", "name": "SEOTechnical", "role": "Technical SEO",     "capabilities": ["crawling", "structured_data", "performance"]},
        {"id": "seo_content",   "name": "SEOContent",   "role": "SEO Content",       "capabilities": ["keywords", "content_optimization", "link_building"]},
    ],
    "marketing": [
        {"id": "marketing_lead",    "name": "MarketingLead",    "role": "Marketing Lead",       "capabilities": ["strategy", "campaigns", "budget"]},
        {"id": "growth_hacker",     "name": "GrowthHacker",     "role": "Growth Hacker",        "capabilities": ["acquisition", "retention", "virality"]},
        {"id": "email_marketer",    "name": "EmailMarketer",    "role": "Email Marketing",      "capabilities": ["newsletters", "sequences", "automation"]},
        {"id": "ads_manager",       "name": "AdsManager",       "role": "Ads Manager",          "capabilities": ["google_ads", "meta_ads", "analytics"]},
        {"id": "content_marketer",  "name": "ContentMarketer",  "role": "Content Marketer",     "capabilities": ["blog", "video", "podcast", "distribution"]},
        {"id": "brand_manager",     "name": "BrandManager",     "role": "Brand Manager",        "capabilities": ["identity", "messaging", "guidelines"]},
    ],
    "social": [
        {"id": "social_lead",     "name": "SocialLead",     "role": "Social Media Lead",    "capabilities": ["strategy", "planning", "analytics"]},
        {"id": "twitter_agent",   "name": "TwitterAgent",   "role": "Twitter/X Manager",    "capabilities": ["tweets", "threads", "engagement"]},
        {"id": "linkedin_agent",  "name": "LinkedInAgent",  "role": "LinkedIn Manager",     "capabilities": ["posts", "articles", "networking"]},
        {"id": "instagram_agent", "name": "InstagramAgent", "role": "Instagram Manager",    "capabilities": ["reels", "stories", "captions"]},
        {"id": "tiktok_agent",    "name": "TikTokAgent",    "role": "TikTok Manager",       "capabilities": ["videos", "trends", "hooks"]},
    ],
    "qa": [
        {"id": "qa_lead",       "name": "QALead",       "role": "QA Lead",             "capabilities": ["test_strategy", "coverage", "reporting"]},
        {"id": "qa_automation", "name": "QAAutomation", "role": "QA Automation",       "capabilities": ["pytest", "selenium", "ci_integration"]},
        {"id": "qa_manual",     "name": "QAManual",     "role": "QA Manual Tester",    "capabilities": ["test_cases", "bug_reports", "ux_testing"]},
    ],
    "devops": [
        {"id": "devops_lead",  "name": "DevOpsLead",  "role": "DevOps Lead",       "capabilities": ["architecture", "ci_cd", "monitoring"]},
        {"id": "cloud_eng",    "name": "CloudEng",    "role": "Cloud Engineer",    "capabilities": ["aws", "gcp", "docker", "kubernetes"]},
        {"id": "sre",          "name": "SRE",         "role": "Site Reliability",  "capabilities": ["uptime", "alerting", "incident_response"]},
    ],
    "security": [
        {"id": "security_lead",  "name": "SecurityLead",  "role": "Security Lead",      "capabilities": ["audits", "policy", "compliance"]},
        {"id": "pen_tester",     "name": "PenTester",     "role": "Penetration Tester", "capabilities": ["vulnerability", "owasp", "reporting"]},
        {"id": "sec_ops",        "name": "SecOps",        "role": "Security Ops",       "capabilities": ["monitoring", "incident", "hardening"]},
    ],
    "documentation": [
        {"id": "doc_lead",      "name": "DocLead",      "role": "Documentation Lead",   "capabilities": ["strategy", "standards", "review"]},
        {"id": "tech_writer",   "name": "TechWriter",   "role": "Technical Writer",     "capabilities": ["api_docs", "guides", "changelogs"]},
        {"id": "doc_trainer",   "name": "DocTrainer",   "role": "Training & Onboarding","capabilities": ["tutorials", "videos", "knowledge_base"]},
    ],
}

# ─────────────────────────────────────────────
# ARBORESCENCE DU PROJET
# ─────────────────────────────────────────────
DIRECTORIES = [
    "backend/api/routes",
    "backend/api/middleware",
    "backend/services",
    "backend/models",
    "backend/database",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/hooks",
    "frontend/src/store",
    "frontend/public",
    "core",
    "agents/cio",
    "agents/development",
    "agents/uiux",
    "agents/seo",
    "agents/marketing",
    "agents/social",
    "agents/qa",
    "agents/devops",
    "agents/security",
    "agents/documentation",
    "config",
    "memory/short_term",
    "memory/long_term",
    "memory/episodic",
    "logs",
    "docs/api",
    "docs/agents",
    "docs/architecture",
    "scripts",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
]

# ─────────────────────────────────────────────
# CONTENU DES FICHIERS DE BASE
# ─────────────────────────────────────────────
FILES = {
    "backend/main.py": '''"""ORION AI - Backend FastAPI"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ORION AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ORION AI is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
''',

    "core/orchestrator.py": '''"""Orchestrateur principal ORION"""
import logging
from typing import Any

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        logger.info("Orchestrateur ORION initialisé")

    def register_agent(self, agent_id: str, agent: Any):
        self.agents[agent_id] = agent
        logger.info(f"Agent enregistré : {agent_id}")

    async def dispatch(self, task: dict) -> dict:
        agent_id = task.get("agent")
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} introuvable"}
        return await self.agents[agent_id].execute(task)
''',

    "core/agent_manager.py": '''"""Gestionnaire des agents ORION"""
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
''',

    "core/ollama_client.py": '''"""Client Ollama pour les modèles locaux"""
import httpx
from typing import AsyncGenerator

OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaClient:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.base_url = OLLAMA_BASE_URL

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60.0
            )
            return response.json().get("response", "")

    async def chat(self, messages: list) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False},
                timeout=60.0
            )
            return response.json().get("message", {}).get("content", "")
''',

    "core/task_router.py": '''"""Router de tâches ORION"""
from typing import Optional

ROUTING_RULES = {
    "code":        "development",
    "seo":         "seo",
    "marketing":   "marketing",
    "social":      "social",
    "test":        "qa",
    "deploy":      "devops",
    "security":    "security",
    "design":      "uiux",
    "doc":         "documentation",
}

class TaskRouter:
    def route(self, task: str) -> Optional[str]:
        task_lower = task.lower()
        for keyword, team in ROUTING_RULES.items():
            if keyword in task_lower:
                return team
        return "cio"  # Orion gère par défaut
''',

    "core/memory.py": '''"""Système de mémoire ORION"""
import json
from pathlib import Path
from datetime import datetime

class Memory:
    def __init__(self):
        self.short_term = {}
        self.long_term_path = Path("memory/long_term")
        self.long_term_path.mkdir(parents=True, exist_ok=True)

    def remember(self, key: str, value: any, permanent: bool = False):
        self.short_term[key] = value
        if permanent:
            file = self.long_term_path / f"{key}.json"
            file.write_text(json.dumps({"key": key, "value": value, "timestamp": str(datetime.now())}))

    def recall(self, key: str) -> any:
        if key in self.short_term:
            return self.short_term[key]
        file = self.long_term_path / f"{key}.json"
        if file.exists():
            return json.loads(file.read_text()).get("value")
        return None

    def forget(self, key: str):
        self.short_term.pop(key, None)
''',

    ".env": '''# ORION AI - Variables d'environnement
# !! Ne jamais commiter ce fichier !!

# API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/orion_ai
REDIS_URL=redis://localhost:6379

# App
APP_ENV=development
APP_SECRET=change_me_in_production
DEBUG=true
''',

    "requirements.txt": '''# ORION AI - Dépendances Python
fastapi==0.111.0
uvicorn[standard]==0.29.0
httpx==0.27.0
pydantic==2.7.0
pydantic-settings==2.2.1
python-dotenv==1.0.1
pyyaml==6.0.1
sqlalchemy==2.0.30
alembic==1.13.1
redis==5.0.4
asyncpg==0.29.0
anthropic==0.26.0
openai==1.30.1
pytest==8.2.0
pytest-asyncio==0.23.7
''',

    "docker-compose.yml": '''version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: orion_ai
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
''',

    "pyproject.toml": '''[tool.poetry]
name = "orion-ai"
version = "1.0.0"
description = "ORION AI - Système multi-agents professionnel"
authors = ["ORION Team"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.111.0"
uvicorn = "^0.29.0"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
''',

    "README.md": '''# 🤖 ORION AI v1.0

Système multi-agents professionnel avec 40 agents spécialisés.

## 🚀 Démarrage rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer l'environnement
cp .env.example .env
# Edite .env avec tes clés API

# 3. Lancer le backend
uvicorn backend.main:app --reload

# 4. Lancer le frontend
cd frontend && npm install && npm run dev
```

## 🏗️ Architecture

- **core/** : Orchestrateur, gestionnaire d'agents, mémoire
- **agents/** : 40 agents YAML spécialisés
- **backend/** : API FastAPI
- **frontend/** : Interface React

## 👥 Les 40 agents

| Équipe        | Agents |
|---------------|--------|
| CIO           | 1      |
| Développement | 10     |
| UI/UX         | 3      |
| SEO           | 3      |
| Marketing     | 6      |
| Réseaux soc.  | 5      |
| QA            | 3      |
| DevOps        | 3      |
| Sécurité      | 3      |
| Documentation | 3      |

## 📄 Licence
MIT
''',

    "config/settings.yaml": '''app:
  name: "ORION AI"
  version: "1.0.0"
  env: "development"

llm:
  default_provider: "ollama"
  ollama:
    url: "http://localhost:11434"
    model: "mistral"
  anthropic:
    model: "claude-sonnet-4-20250514"

memory:
  short_term_ttl: 3600
  long_term_enabled: true

logging:
  level: "INFO"
  format: "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
''',

    "scripts/install.sh": '''#!/bin/bash
echo "🤖 Installation ORION AI..."
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env .env.backup
echo "✅ Installation terminée !"
echo "👉 Configure ton fichier .env puis lance : uvicorn backend.main:app --reload"
''',

    "scripts/install.ps1": '''# Installation ORION AI (Windows)
Write-Host "🤖 Installation ORION AI..." -ForegroundColor Cyan
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✅ Installation terminée !" -ForegroundColor Green
Write-Host "👉 Configure ton fichier .env puis lance : uvicorn backend.main:app --reload"
''',
}

# ─────────────────────────────────────────────
# FONCTIONS DE GÉNÉRATION
# ─────────────────────────────────────────────
def create_directories(base: Path):
    print("\n📁 Création des dossiers...")
    for d in DIRECTORIES:
        path = base / d
        path.mkdir(parents=True, exist_ok=True)
        (path / ".gitkeep").touch()
    print(f"   ✅ {len(DIRECTORIES)} dossiers créés")

def create_agent_yaml(base: Path):
    print("\n🤖 Génération des fichiers agents YAML...")
    count = 0
    for team, agents in AGENTS.items():
        team_dir = base / "agents" / team
        team_dir.mkdir(parents=True, exist_ok=True)
        for agent in agents:
            yaml_content = {
                "id": agent["id"],
                "name": agent["name"],
                "role": agent.get("role", ""),
                "team": team,
                "description": agent.get("description", f"Agent {agent['name']} de l'équipe {team}"),
                "capabilities": agent.get("capabilities", []),
                "model": "mistral",
                "memory_enabled": True,
                "tools": [],
                "system_prompt": f"Tu es {agent['name']}, {agent.get('role', '')} dans ORION AI. Tu es expert en {', '.join(agent.get('capabilities', []))}. Tu travailles en équipe avec les autres agents ORION pour accomplir des tâches complexes.",
            }
            yaml_file = team_dir / f"{agent['id']}.yaml"
            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(yaml_content, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            count += 1
    print(f"   ✅ {count} fichiers agents créés")

def create_base_files(base: Path):
    print("\n📄 Génération des fichiers de base...")
    count = 0
    for rel_path, content in FILES.items():
        file_path = base / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        count += 1
    print(f"   ✅ {count} fichiers créés")

def create_gitignore(base: Path):
    content = """# Python
__pycache__/
*.py[cod]
*.egg
dist/
build/
*.egg-info/
venv/
.venv/

# Env
.env
*.env.local

# Logs
logs/
*.log

# DB
*.sqlite3

# Node
node_modules/
.next/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""
    (base / ".gitignore").write_text(content)

def print_summary(base: Path):
    total_agents = sum(len(v) for v in AGENTS.values())
    print("\n" + "═" * 50)
    print("🎉 ORION AI v1.0 généré avec succès !")
    print("═" * 50)
    print(f"📁 Dossiers   : {len(DIRECTORIES)}")
    print(f"🤖 Agents     : {total_agents}")
    print(f"📄 Fichiers   : {len(FILES)}")
    print(f"📍 Localisation : {base.resolve()}")
    print("\n🚀 Prochaines étapes :")
    print("   1. cd", base.resolve())
    print("   2. pip install -r requirements.txt")
    print("   3. Configure ton .env")
    print("   4. uvicorn backend.main:app --reload")
    print("═" * 50 + "\n")

# ─────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────
def main():
    print("═" * 50)
    print("🤖 ORION AI v1.0 - Générateur de projet")
    print("═" * 50)

    base = Path(".")

    create_directories(base)
    create_agent_yaml(base)
    create_base_files(base)
    create_gitignore(base)
    print_summary(base)

if __name__ == "__main__":
    main()
