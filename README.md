# KURO Performance - Postural Assessment System

Aplikasi GUI berbasis Python untuk analisis postural menggunakan YOLO (You Only Look Once) untuk mendeteksi dan menganalisis postur tubuh manusia.

## Fitur Utama

### 1. Dashboard Welcome (Dashboard 1)
- Input data pengguna (Name dan Height)
- Tampilan logo KURO Performance
- Desain modern dengan tema hitam dan biru

### 2. Dashboard Menu Utama (Dashboard 2)
- Upload gambar (single atau multiple)
- Upload model YOLO (.pt format)
- Pengaturan confidence threshold dengan slider
- Preview gambar yang diupload
- Menu navigasi:
  - Analisis Single Images
  - Analisis Batch Images
  - System Info
  - Keluar

### 3. Dashboard Visualisasi (Dashboard 3)
- Perbandingan gambar Before dan After analisis
- Tampilan bounding box dan keypoints
- Summary hasil analisis singkat
- Navigasi ke detailed results

### 4. Dashboard Report Detail (Dashboard 4)
- Gambar dengan anotasi lengkap
- Grafik visualisasi (Shoulder, Hip, Spine, Head analysis)
- Tabel hasil analisis imbalance postural dengan kolom:
  - Komponen
  - Parameter
  - Nilai
  - Satuan
  - Status
  - Score
- Export hasil ke CSV
- Laporan klasifikasi dan rekomendasi

## Klasifikasi Postural

Sistem mendukung deteksi dan klasifikasi postur berikut:

- **Normal**: Normal-Kanan, Normal-Kiri, Normal-Belakang, Normal-Depan
- **Kyphosis**: Kyphosis-Kanan, Kyphosis-Kiri, Kyphosis-Belakang, Kyphosis-Depan
- **Lordosis**: Lordosis-Kanan, Lordosis-Kiri, Lordosis-Belakang, Lordosis-Depan
- **Swayback**: Swayback-Kanan, Swayback-Kiri, Swayback-Belakang, Swayback-Depan

## Jenis Analisis

### Back/Front Analysis
Menganalisis postur dari sudut depan/belakang dengan parameter:
- Shoulder Imbalance (mm)
- Hip Imbalance (mm)
- Spine Deviation (mm)
- Shoulder Angle (derajat)
- Hip Angle (derajat)
- Posture Score (0-100)

### Side Analysis
Menganalisis postur dari sudut samping dengan parameter:
- Head Shift (mm)
- Head Tilt (derajat)
- Posture Score (0-100)

## Struktur Project

```
project1/
├── assets/
│   ├── kuro_logo.png
│   └── kuro_rebranding_icon_full_clr_online.png
├── src/
│   ├── main.py                    # Entry point aplikasi
│   ├── config.py                  # Konfigurasi global
│   ├── dashboards/
│   │   ├── dashboard1.py          # Welcome screen
│   │   ├── dashboard2.py          # Main menu
│   │   ├── dashboard3.py          # Visualization
│   │   └── dashboard4.py          # Detailed report
│   ├── analysis/
│   │   ├── yolo_analyzer.py       # YOLO detection engine
│   │   └── posture_calculator.py  # Posture calculation
│   └── utils/
│       ├── database.py            # Supabase integration
│       ├── visualization.py       # Chart generation
│       └── export.py              # CSV export
├── models/                        # YOLO model files (.pt)
├── temp/                          # Temporary files
├── requirements.txt
├── .env.example
└── README.md
```

## Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd project1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Buat file `.env` di root directory:

```bash
cp .env.example .env
```

Edit `.env` dan isi dengan credentials Supabase Anda:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### 4. Setup Database

Database schema akan otomatis dibuat menggunakan Supabase migration.

Tabel yang dibuat:
- `user_sessions`: Menyimpan data sesi pengguna
- `analysis_results`: Menyimpan hasil analisis

## Cara Menggunakan

### 1. Jalankan Aplikasi

```bash
python -m src.main
```

### 2. Workflow Analisis

#### Step 1: Input Data Pengguna
- Masukkan nama
- Masukkan tinggi badan (dalam mm, contoh: 1700 untuk 170cm)
- Klik "Mulai Analisis"

#### Step 2: Upload dan Konfigurasi
- Upload gambar postur yang akan dianalisis
- Upload model YOLO (.pt file)
- Atur confidence threshold (0.0 - 1.0)
- Pilih mode analisis:
  - Single: Analisis satu gambar
  - Batch: Analisis multiple gambar

#### Step 3: Analisis
- Klik "ANALYZE IMAGES"
- Tunggu proses analisis selesai

#### Step 4: Review Hasil
- Dashboard 3 menampilkan perbandingan Before/After
- Klik "View Detailed Results" untuk laporan lengkap

#### Step 5: Export Hasil
- Di Dashboard 4, review semua detail analisis
- Klik "Export to CSV" untuk menyimpan hasil

## Integrasi dengan YOLO

### Format Model

Aplikasi ini menggunakan model YOLO dengan format `.pt` (PyTorch).

Model harus memiliki kemampuan:
- Object Detection untuk postur tubuh
- Keypoint Detection untuk 17 titik keypoints:
  - 0: nose
  - 1-2: left_eye, right_eye
  - 3-4: left_ear, right_ear
  - 5-6: left_shoulder, right_shoulder
  - 7-8: left_elbow, right_elbow
  - 9-10: left_wrist, right_wrist
  - 11-12: left_hip, right_hip
  - 13-14: left_knee, right_knee
  - 15-16: left_ankle, right_ankle

### Output yang Diharapkan

Model YOLO harus menghasilkan output dengan format:
- Bounding boxes untuk deteksi postur
- Confidence scores
- Class labels (sesuai klasifikasi postural)
- Keypoints coordinates dan confidence

## Integrasi dengan Website

Aplikasi ini dapat diintegrasikan dengan website menggunakan beberapa pendekatan:

### 1. REST API Integration
Convert aplikasi menjadi REST API menggunakan FastAPI atau Flask:

```python
from fastapi import FastAPI, UploadFile
app = FastAPI()

@app.post("/analyze")
async def analyze_posture(image: UploadFile, model: str, confidence: float):
    # Run analysis logic
    return {"results": analysis_results}
```

### 2. Web Framework Integration
Gunakan framework seperti Django atau Flask untuk membuat web interface:
- Upload gambar melalui form HTML
- Process di backend menggunakan analysis engine
- Tampilkan hasil di halaman web

### 3. Streamlit Integration
Convert ke Streamlit untuk web app yang lebih cepat:

```python
import streamlit as st

st.title("KURO Performance - Postural Assessment")
uploaded_file = st.file_uploader("Upload Image")
if uploaded_file:
    # Run analysis
    st.image(annotated_image)
```

## Database Schema

### Table: user_sessions
```sql
CREATE TABLE user_sessions (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  height numeric NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

### Table: analysis_results
```sql
CREATE TABLE analysis_results (
  id uuid PRIMARY KEY,
  session_id uuid REFERENCES user_sessions(id),
  analysis_type text NOT NULL,
  classification text NOT NULL,
  confidence numeric,
  score numeric,
  measurements jsonb,
  keypoints jsonb,
  image_path text,
  created_at timestamptz DEFAULT now()
);
```

## Troubleshooting

### Error: "No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**MacOS:**
```bash
brew install python-tk
```

### Error: "Could not load image"

Pastikan file gambar ada di path yang benar dan format didukung (jpg, png, bmp).

### Error: "Model not found"

Pastikan file model YOLO (.pt) sudah diupload dan path-nya benar.

### Error: "Supabase connection failed"

Periksa:
- File `.env` sudah dibuat
- SUPABASE_URL dan SUPABASE_KEY sudah benar
- Koneksi internet aktif

## Kontribusi

Untuk berkontribusi:
1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## License

Copyright 2025 KURO Performance. All rights reserved.

## Support

Untuk pertanyaan atau dukungan, hubungi tim KURO Performance.

## Changelog

### Version 1.0.0 (2025-01-07)
- Initial release
- Dashboard 1-4 lengkap
- YOLO integration
- Posture analysis engine
- CSV export functionality
- Supabase database integration