@echo off
echo Starting Credit-It FastAPI Backend Server...
cd /d "%~dp0"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
