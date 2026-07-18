#!/bin/bash
echo "🤖 Installation ORION AI..."
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env .env.backup
echo "✅ Installation terminée !"
echo "👉 Configure ton fichier .env puis lance : uvicorn backend.main:app --reload"
