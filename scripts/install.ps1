# Installation ORION AI (Windows)
Write-Host "🤖 Installation ORION AI..." -ForegroundColor Cyan
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✅ Installation terminée !" -ForegroundColor Green
Write-Host "👉 Configure ton fichier .env puis lance : uvicorn backend.main:app --reload"
