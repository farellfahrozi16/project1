# Integration Guide - KURO Performance Postural Assessment

Panduan lengkap untuk mengintegrasikan aplikasi KURO Performance Postural Assessment ke dalam berbagai platform.

## Table of Contents
1. [Web Integration](#web-integration)
2. [REST API Development](#rest-api-development)
3. [Streamlit Web App](#streamlit-web-app)
4. [Django Integration](#django-integration)
5. [Flask Integration](#flask-integration)

## Web Integration

### Approach 1: REST API Backend + Web Frontend

Aplikasi desktop dapat dikonversi menjadi REST API yang dapat diakses oleh web frontend.

#### Backend API (FastAPI)

```python
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from src.analysis.yolo_analyzer import YOLOPostureAnalyzer
from src.analysis.posture_calculator import PostureCalculator
import uuid

app = FastAPI(title="KURO Postural Assessment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/api/analyze")
async def analyze_posture(
    image: UploadFile = File(...),
    name: str = Form(...),
    height: float = Form(...),
    model_path: str = Form(...),
    confidence: float = Form(0.25)
):
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{image.filename}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    analyzer = YOLOPostureAnalyzer(model_path)
    calculator = PostureCalculator(height)

    analysis_data = analyzer.analyze_image(str(file_path), confidence)

    results = []
    for detection in analysis_data["detections"]:
        classification = detection["classification"]
        keypoints = detection["keypoints"]

        analysis_type = calculator.determine_analysis_type(classification)
        metrics = calculator.calculate_posture_metrics(keypoints, analysis_type)

        results.append({
            "classification": classification,
            "confidence": detection["confidence"],
            "metrics": metrics,
            "score": metrics.get("score", 0.0)
        })

    return {
        "success": True,
        "user": {"name": name, "height": height},
        "results": results
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
```

#### Frontend (React Example)

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function PostureAnalysis() {
  const [name, setName] = useState('');
  const [height, setHeight] = useState('');
  const [image, setImage] = useState(null);
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);
    formData.append('name', name);
    formData.append('height', height);
    formData.append('model_path', '/path/to/model.pt');
    formData.append('confidence', 0.25);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/analyze',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResults(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  return (
    <div className="container">
      <h1>KURO Postural Assessment</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Height (mm)"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Analyze</button>
      </form>

      {results && (
        <div className="results">
          <h2>Analysis Results</h2>
          {results.results.map((result, idx) => (
            <div key={idx}>
              <p>Classification: {result.classification}</p>
              <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
              <p>Score: {result.score}/100</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PostureAnalysis;
```

## Streamlit Web App

Streamlit adalah cara tercepat untuk membuat web app dari Python code.

### Installation

```bash
pip install streamlit
```

### Streamlit App

```python
import streamlit as st
from PIL import Image
import cv2
import numpy as np
from src.analysis.yolo_analyzer import YOLOPostureAnalyzer
from src.analysis.posture_calculator import PostureCalculator
from src.utils.visualization import PostureVisualizer
from src.utils.export import ResultExporter

st.set_page_config(
    page_title="KURO Postural Assessment",
    page_icon="🦴",
    layout="wide"
)

st.title("🦴 KURO Performance - Postural Assessment")
st.markdown("---")

with st.sidebar:
    st.header("User Information")
    name = st.text_input("Name")
    height = st.number_input("Height (mm)", min_value=1000, max_value=2500, value=1700)

    st.header("Analysis Settings")
    model_path = st.text_input("Model Path", value="models/posture_model.pt")
    confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

st.header("📸 Upload Image")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None and name and model_path:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

    if st.button("🔍 Analyze Posture", type="primary"):
        with st.spinner("Analyzing..."):
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            analyzer = YOLOPostureAnalyzer(model_path)
            calculator = PostureCalculator(height)

            analysis_data = analyzer.analyze_image(temp_path, confidence)

            if analysis_data["detections"]:
                detection = analysis_data["detections"][0]
                classification = detection["classification"]
                keypoints = detection["keypoints"]

                analysis_type = calculator.determine_analysis_type(classification)
                metrics = calculator.calculate_posture_metrics(keypoints, analysis_type)

                annotated_image = analyzer.annotate_image(temp_path, analysis_data)

                with col2:
                    st.subheader("Analyzed Image")
                    img_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                    st.image(img_rgb, use_column_width=True)

                st.markdown("---")
                st.header("📊 Analysis Results")

                col3, col4, col5 = st.columns(3)
                with col3:
                    st.metric("Classification", classification)
                with col4:
                    st.metric("Confidence", f"{detection['confidence']:.2%}")
                with col5:
                    st.metric("Score", f"{metrics.get('score', 0):.1f}/100")

                st.subheader("📏 Measurements")

                if analysis_type == "back_front_analysis":
                    col6, col7, col8 = st.columns(3)
                    with col6:
                        st.metric("Shoulder Imbalance", f"{metrics.get('shoulder_imbalance', 0):.1f} mm")
                    with col7:
                        st.metric("Hip Imbalance", f"{metrics.get('hip_imbalance', 0):.1f} mm")
                    with col8:
                        st.metric("Spine Deviation", f"{metrics.get('spine_deviation', 0):.1f} mm")

                elif analysis_type == "side_analysis":
                    col6, col7 = st.columns(2)
                    with col6:
                        st.metric("Head Shift", f"{metrics.get('head_shift', 0):.1f} mm")
                    with col7:
                        st.metric("Head Tilt", f"{metrics.get('head_tilt', 0):.1f}°")

                exporter = ResultExporter()
                df = exporter.create_analysis_table(metrics, analysis_type)

                st.subheader("📋 Detailed Report")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Report (CSV)",
                    data=csv,
                    file_name=f"posture_analysis_{name}.csv",
                    mime="text/csv"
                )

                recommendation = exporter.format_recommendation(classification, metrics.get('score', 0))
                st.info(recommendation)
            else:
                st.error("No detections found. Please try another image or adjust confidence threshold.")

st.markdown("---")
st.markdown("© 2025 KURO Performance. All rights reserved.")
```

### Run Streamlit App

```bash
streamlit run streamlit_app.py
```

## Django Integration

### Django Views

```python
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from src.analysis.yolo_analyzer import YOLOPostureAnalyzer
from src.analysis.posture_calculator import PostureCalculator
import json

@csrf_exempt
def analyze_posture(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        height = float(request.POST.get('height'))
        image = request.FILES.get('image')
        model_path = request.POST.get('model_path')
        confidence = float(request.POST.get('confidence', 0.25))

        file_path = default_storage.save(f'uploads/{image.name}', image)
        full_path = default_storage.path(file_path)

        analyzer = YOLOPostureAnalyzer(model_path)
        calculator = PostureCalculator(height)

        analysis_data = analyzer.analyze_image(full_path, confidence)

        results = []
        for detection in analysis_data["detections"]:
            classification = detection["classification"]
            keypoints = detection["keypoints"]

            analysis_type = calculator.determine_analysis_type(classification)
            metrics = calculator.calculate_posture_metrics(keypoints, analysis_type)

            results.append({
                "classification": classification,
                "confidence": detection["confidence"],
                "metrics": metrics,
                "score": metrics.get("score", 0.0)
            })

        return JsonResponse({
            'success': True,
            'user': {'name': name, 'height': height},
            'results': results
        })

    return render(request, 'posture/analyze.html')

def index(request):
    return render(request, 'posture/index.html')
```

### Django Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>KURO Postural Assessment</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #3FB5E5;
            color: white;
            cursor: pointer;
            border: none;
        }
        button:hover {
            background: #2A9CD6;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦴 KURO Performance - Postural Assessment</h1>

        <form id="analysisForm" enctype="multipart/form-data">
            <div class="form-group">
                <label>Name:</label>
                <input type="text" name="name" required>
            </div>

            <div class="form-group">
                <label>Height (mm):</label>
                <input type="number" name="height" required>
            </div>

            <div class="form-group">
                <label>Upload Image:</label>
                <input type="file" name="image" accept="image/*" required>
            </div>

            <button type="submit">Analyze Posture</button>
        </form>

        <div id="results" class="results" style="display:none;"></div>
    </div>

    <script>
        document.getElementById('analysisForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(e.target);
            formData.append('model_path', '/path/to/model.pt');
            formData.append('confidence', '0.25');

            const response = await fetch('/analyze/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                const resultsDiv = document.getElementById('results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `
                    <h2>Analysis Results</h2>
                    ${data.results.map(r => `
                        <div>
                            <h3>${r.classification}</h3>
                            <p>Confidence: ${(r.confidence * 100).toFixed(1)}%</p>
                            <p>Score: ${r.score.toFixed(1)}/100</p>
                        </div>
                    `).join('')}
                `;
            }
        });
    </script>
</body>
</html>
```

## Flask Integration

```python
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.analysis.yolo_analyzer import YOLOPostureAnalyzer
from src.analysis.posture_calculator import PostureCalculator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    name = request.form.get('name')
    height = float(request.form.get('height'))
    model_path = request.form.get('model_path', 'models/posture_model.pt')
    confidence = float(request.form.get('confidence', 0.25))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    analyzer = YOLOPostureAnalyzer(model_path)
    calculator = PostureCalculator(height)

    analysis_data = analyzer.analyze_image(filepath, confidence)

    results = []
    for detection in analysis_data["detections"]:
        classification = detection["classification"]
        keypoints = detection["keypoints"]

        analysis_type = calculator.determine_analysis_type(classification)
        metrics = calculator.calculate_posture_metrics(keypoints, analysis_type)

        results.append({
            "classification": classification,
            "confidence": detection["confidence"],
            "metrics": metrics,
            "score": metrics.get("score", 0.0)
        })

    return jsonify({
        'success': True,
        'user': {'name': name, 'height': height},
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./uploads:/app/uploads
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
```

## Conclusion

Aplikasi KURO Performance dapat diintegrasikan dengan berbagai platform web menggunakan pendekatan yang sesuai dengan kebutuhan:

- **REST API**: Untuk aplikasi modern dengan frontend terpisah
- **Streamlit**: Untuk prototype dan demo cepat
- **Django/Flask**: Untuk aplikasi web full-stack

Pilih pendekatan yang paling sesuai dengan infrastruktur dan kebutuhan Anda.
