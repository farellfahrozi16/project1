#!/bin/bash

echo "====================================="
echo "Git Repository Initialization"
echo "====================================="
echo ""

if [ -d .git ]; then
    echo "Git repository already exists!"
    exit 1
fi

echo "Initializing git repository..."
git init

echo "Adding files to git..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit: KURO Performance Postural Assessment System v1.0.0

Features:
- Dashboard 1: Welcome screen with user data input
- Dashboard 2: Main menu with image/model upload
- Dashboard 3: Before/After visualization
- Dashboard 4: Detailed report with CSV export
- YOLO integration for posture detection
- Supabase database integration
- Complete documentation

Technologies:
- Python 3.10+
- Tkinter GUI
- Ultralytics YOLO
- OpenCV
- Matplotlib
- Pandas
- Supabase
"

echo ""
echo "====================================="
echo "Git repository initialized!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Create a repository on GitHub"
echo "2. Add remote: git remote add origin <repository-url>"
echo "3. Push to GitHub: git push -u origin main"
echo ""
