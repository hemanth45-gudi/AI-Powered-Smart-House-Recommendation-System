Write-Host "Starting Backend API..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "pip install -r apps\backend_api\requirements.txt; python -m uvicorn apps.backend_api.main:app --reload --port 8000"

Write-Host "Starting ML Engine..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "pip install -r apps\ml_engine\requirements.txt; python -m uvicorn apps.ml_engine.main:app --reload --port 8001"

Write-Host "Starting Mobile App..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\mobile_app; flutter run"
