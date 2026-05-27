@echo off
echo Setting up Sorting Visualizer...

if not exist venv\ (
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"

echo Setup complete. Run scripts\run.bat to start.
pause
