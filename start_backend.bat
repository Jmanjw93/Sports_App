@echo off
echo Starting Sports Analytics Backend on port 8001...
cd backend
python -m uvicorn app.main:app --reload --port 8001
pause
