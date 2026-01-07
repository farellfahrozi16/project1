#!/bin/bash

echo "Starting KURO Performance Postural Assessment..."

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup.sh
fi

source venv/bin/activate

python run.py
