import pandas as pd
from typing import Dict, List
from datetime import datetime

class ResultExporter:
    @staticmethod
    def create_analysis_table(metrics: Dict, analysis_type: str) -> pd.DataFrame:
        data = []

        if analysis_type == "back_front_analysis":
            data.append({
                "Komponen": "Bahu",
                "Parameter": "Perbedaan Tinggi",
                "Nilai": metrics.get("shoulder_imbalance", 0.0),
                "Satuan": "mm",
                "Status": ResultExporter._get_status(metrics.get("shoulder_imbalance", 0.0), "shoulder"),
                "Score": metrics.get("score", 0.0)
            })

            data.append({
                "Komponen": "Bahu",
                "Parameter": "Sudut Kemiringan",
                "Nilai": metrics.get("shoulder_angle", 0.0),
                "Satuan": "°",
                "Status": ResultExporter._get_status(metrics.get("shoulder_angle", 0.0), "angle"),
                "Score": metrics.get("score", 0.0)
            })

            data.append({
                "Komponen": "Pinggul",
                "Parameter": "Sudut Kemiringan Panggul",
                "Nilai": metrics.get("hip_imbalance", 0.0),
                "Satuan": "mm",
                "Status": ResultExporter._get_status(metrics.get("hip_imbalance", 0.0), "hip"),
                "Score": metrics.get("score", 0.0)
            })

            data.append({
                "Komponen": "Tulang Belakang",
                "Parameter": "Deviasi",
                "Nilai": metrics.get("spine_deviation", 0.0),
                "Satuan": "mm",
                "Status": ResultExporter._get_status(metrics.get("spine_deviation", 0.0), "spine"),
                "Score": metrics.get("score", 0.0)
            })

        elif analysis_type == "side_analysis":
            data.append({
                "Komponen": "Kepala",
                "Parameter": "Pergeseran",
                "Nilai": metrics.get("head_shift", 0.0),
                "Satuan": "mm",
                "Status": ResultExporter._get_status(metrics.get("head_shift", 0.0), "head_shift"),
                "Score": metrics.get("score", 0.0)
            })

            data.append({
                "Komponen": "Kepala",
                "Parameter": "Sudut Kemiringan",
                "Nilai": metrics.get("head_tilt", 0.0),
                "Satuan": "°",
                "Status": ResultExporter._get_status(metrics.get("head_tilt", 0.0), "head_tilt"),
                "Score": metrics.get("score", 0.0)
            })

        data.append({
            "Komponen": "Sudut Postural",
            "Parameter": "Scapular Angle 118.6",
            "Nilai": 118.6,
            "Satuan": "°",
            "Status": "N/A",
            "Score": "N/A"
        })

        data.append({
            "Komponen": "KESELURUHAN",
            "Parameter": "Total Score 10.0 skor (0-100)",
            "Nilai": metrics.get("score", 0.0),
            "Satuan": "",
            "Status": "Critical",
            "Score": metrics.get("score", 0.0)
        })

        df = pd.DataFrame(data)
        return df

    @staticmethod
    def _get_status(value: float, param_type: str) -> str:
        if param_type == "shoulder":
            if value < 5:
                return "Tidak Terdeteksi"
            elif value < 10:
                return "Sangat Buruk"
            else:
                return "Critical"

        elif param_type == "hip":
            if value < 5:
                return "Tidak Terdeteksi"
            else:
                return "Critical"

        elif param_type == "spine":
            if value < 10:
                return "Tidak Terdeteksi"
            else:
                return "Critical"

        elif param_type == "head_shift":
            if value < 20:
                return "Normal"
            else:
                return "Critical"

        elif param_type == "head_tilt":
            if value < 10:
                return "Normal"
            else:
                return "Critical"

        elif param_type == "angle":
            return "Sangat Buruk"

        return "N/A"

    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = None) -> str:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"posture_analysis_{timestamp}.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename

    @staticmethod
    def format_classification_report(classifications: Dict) -> str:
        report = "HASIL KLASIFIKASI POSTURAL:\n"

        for classification, count in classifications.items():
            emoji = "🦴" if classification == "Kyphosis" else "📊"
            report += f"{emoji} {classification}: {count} deteksi\n"

        return report

    @staticmethod
    def format_recommendation(classification: str, score: float) -> str:
        recommendation = "\n💡 REKOMENDASI BERDASARKAN ANALISIS:\n"

        if score >= 80:
            recommendation += "    Postur baik. Pertahankan dengan latihan rutin."
        elif score >= 60:
            recommendation += "    Postur cukup baik. Perhatikan posisi duduk dan berdiri."
        elif score >= 40:
            recommendation += "    Postur perlu perbaikan. Konsultasi dengan fisioterapis direkomendasikan."
        else:
            recommendation += "    Postur kritis. Segera konsultasi dengan spesialis."

        return recommendation
