# 🤖 ORION AI v1.0

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
