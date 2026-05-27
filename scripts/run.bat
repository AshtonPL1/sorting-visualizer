@echo off
call venv\Scripts\activate.bat
python -m src.ui.console_ui --interactive
pause
