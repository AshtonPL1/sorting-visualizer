#!/usr/bin/env bash
set -e

echo "Setting up Sorting Visualizer..."

# Create virtual environment if missing
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"

echo "Setup complete. Run scripts/run.sh to start."
