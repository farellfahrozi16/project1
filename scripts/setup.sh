#!/bin/bash

echo "====================================="
echo "KURO Performance Setup Script"
echo "====================================="
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Step 4: Creating necessary directories..."
mkdir -p models
mkdir -p temp
mkdir -p uploads

echo "Step 5: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env file with your Supabase credentials"
fi

echo ""
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Supabase credentials"
echo "2. Place your YOLO model (.pt file) in the models/ directory"
echo "3. Run the application: python run.py"
echo ""
