Write-Host "Starting Backend API..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\backend_api; pip install -r requirements.txt; uvicorn main:app --reload --port 8000"

Write-Host "Starting ML Engine..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\ml_engine; pip install -r requirements.txt; uvicorn main:app --reload --port 8001"

Write-Host "Starting Mobile App..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\mobile_app; flutter run"
