# Quick Start Guide

Panduan cepat untuk memulai menggunakan KURO Performance Postural Assessment System.

## Prerequisites

- Python 3.10 atau lebih tinggi
- pip (Python package manager)
- Git
- YOLO model file (.pt format)
- Supabase account (opsional, untuk database persistence)

## Installation (5 menit)

### Option 1: Automated Setup (Recommended)

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual Setup

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

mkdir -p models temp uploads

cp .env.example .env
```

## Configuration (2 menit)

### 1. Edit .env file

```bash
nano .env
```

Isi dengan credentials Supabase Anda:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 2. Add YOLO Model

Place your YOLO model file in the `models/` directory:

```bash
cp /path/to/your/model.pt models/
```

## Running the Application

### Option 1: Using run script

```bash
./scripts/run_dev.sh
```

### Option 2: Direct Python

```bash
python run.py
```

### Option 3: Python module

```bash
python -m src.main
```

## First Time Usage

### Step 1: Welcome Screen
1. Masukkan nama Anda
2. Masukkan tinggi badan dalam mm (contoh: 1700 untuk 170cm)
3. Klik "Mulai Analisis"

### Step 2: Upload and Configure
1. Klik "Browse Images" untuk upload gambar
2. Klik "Browse Model" untuk pilih YOLO model (.pt file)
3. Atur confidence threshold (default: 0.25)
4. Preview gambar akan muncul di bawah

### Step 3: Analyze
1. Klik tombol "ANALYZE IMAGES"
2. Tunggu proses analisis (progress bar akan muncul)

### Step 4: View Results
1. Dashboard 3 akan menampilkan Before/After comparison
2. Klik "View Detailed Results" untuk laporan lengkap

### Step 5: Export
1. Di Dashboard 4, review semua hasil
2. Klik "Export to CSV" untuk save report

## Testing the Application

### Test with Sample Image

```bash
curl -o test_image.jpg https://example.com/sample-posture.jpg

cp test_image.jpg uploads/
```

Run the application and upload the test image.

## Troubleshooting

### Error: "No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Reinstall Python with "tcl/tk and IDLE" option checked.

### Error: "Model file not found"

Make sure your YOLO model is in the `models/` directory:

```bash
ls -la models/
```

### Error: "Cannot connect to Supabase"

1. Check your `.env` file exists
2. Verify SUPABASE_URL and SUPABASE_KEY are correct
3. Test internet connection

### Application won't start

```bash
python -c "import tkinter; print('Tkinter OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import ultralytics; print('YOLO OK')"
```

If any import fails, reinstall that package:

```bash
pip install --upgrade opencv-python ultralytics
```

## Common Commands

### Check Python version
```bash
python --version
```

### Update dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clean temporary files
```bash
rm -rf temp/*
rm -rf uploads/*
```

### View logs
```bash
tail -f app.log
```

## Git Repository Setup

### Initialize Git
```bash
./scripts/init_git.sh
```

### Push to GitHub
```bash
git remote add origin https://github.com/yourusername/kuro-posture.git
git branch -M main
git push -u origin main
```

## File Structure Overview

```
project1/
├── src/                      # Source code
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── dashboards/          # GUI dashboards
│   ├── analysis/            # Analysis engines
│   └── utils/               # Utility functions
├── assets/                   # Images and logos
├── models/                   # YOLO models (.pt files)
├── scripts/                  # Setup and run scripts
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                # Full documentation
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for web integration
3. Review [CHANGELOG.md](CHANGELOG.md) for version history

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review the full README.md
3. Check GitHub issues
4. Contact KURO Performance support team

## Tips for Best Results

1. Use high-quality images (min 1920x1080)
2. Ensure good lighting in photos
3. Subject should be centered in frame
4. Use confidence threshold 0.25-0.50 for best accuracy
5. Calibrate height input accurately (in millimeters)

## Performance Optimization

For faster analysis:
- Use GPU-enabled YOLO model if available
- Resize large images before upload
- Close other heavy applications
- Use SSD for model and image storage

## Keyboard Shortcuts

Currently no keyboard shortcuts implemented. Feature coming in v2.0.

## Default Values

- Confidence Threshold: 0.25
- Image Format: JPG, PNG, BMP
- Model Format: .pt (PyTorch)
- Height Unit: millimeters (mm)
- Score Range: 0-100

Enjoy using KURO Performance Postural Assessment System!
