import numpy as np
import math
from typing import Dict, Tuple, Optional

class PostureCalculator:
    def __init__(self, actual_height_mm: float):
        self.actual_height_mm = actual_height_mm
        self.ratio_mm_per_pixel = None

    def calculate_posture_metrics(self, keypoints: Dict, analysis_type: str) -> Dict:
        if not keypoints:
            return self._empty_metrics()

        self._estimate_ratio(keypoints)

        if analysis_type == "back_front_analysis":
            return self._calculate_back_front_metrics(keypoints)
        elif analysis_type == "side_analysis":
            return self._calculate_side_metrics(keypoints)
        else:
            return self._empty_metrics()

    def _estimate_ratio(self, keypoints: Dict):
        estimated_height_pixels = self._estimate_person_height(keypoints)

        if estimated_height_pixels > 0:
            self.ratio_mm_per_pixel = self.actual_height_mm / estimated_height_pixels
        else:
            default_height_pixels = 5712
            self.ratio_mm_per_pixel = self.actual_height_mm / default_height_pixels

    def _estimate_person_height(self, keypoints: Dict) -> float:
        head_parts = ["nose", "left_eye", "right_eye", "left_ear", "right_ear"]
        feet_parts = ["left_ankle", "right_ankle"]

        head_points = []
        for part in head_parts:
            if part in keypoints:
                x, y = keypoints[part]["position"]
                head_points.append(y)

        feet_points = []
        for part in feet_parts:
            if part in keypoints:
                x, y = keypoints[part]["position"]
                feet_points.append(y)

        if head_points and feet_points:
            top_y = min(head_points)
            bottom_y = max(feet_points)
            return abs(bottom_y - top_y)

        return 0

    def _calculate_back_front_metrics(self, keypoints: Dict) -> Dict:
        metrics = {
            "ratio": self.ratio_mm_per_pixel,
            "shoulder_imbalance": 0.0,
            "hip_imbalance": 0.0,
            "spine_deviation": 0.0,
            "shoulder_angle": 0.0,
            "hip_angle": 0.0,
            "score": 0.0
        }

        if "left_shoulder" in keypoints and "right_shoulder" in keypoints:
            shoulder_diff_pixels, shoulder_angle = self._calculate_height_difference_and_angle(
                keypoints["left_shoulder"]["position"],
                keypoints["right_shoulder"]["position"]
            )

            shoulder_diff_mm = abs(shoulder_diff_pixels * self.ratio_mm_per_pixel)

            if shoulder_diff_pixels > 50:
                shoulder_diff_mm = min(shoulder_diff_mm, 50.0)

            metrics["shoulder_imbalance"] = round(shoulder_diff_mm, 1)
            metrics["shoulder_angle"] = round(shoulder_angle, 1)

        if "left_hip" in keypoints and "right_hip" in keypoints:
            hip_diff_pixels, hip_angle = self._calculate_height_difference_and_angle(
                keypoints["left_hip"]["position"],
                keypoints["right_hip"]["position"]
            )
            metrics["hip_imbalance"] = round(abs(hip_diff_pixels * self.ratio_mm_per_pixel), 1)
            metrics["hip_angle"] = round(hip_angle, 1)

        if "left_shoulder" in keypoints and "right_shoulder" in keypoints and \
           "left_hip" in keypoints and "right_hip" in keypoints:
            spine_deviation = self._calculate_spine_deviation(
                keypoints["left_shoulder"]["position"],
                keypoints["right_shoulder"]["position"],
                keypoints["left_hip"]["position"],
                keypoints["right_hip"]["position"]
            )
            metrics["spine_deviation"] = round(abs(spine_deviation * self.ratio_mm_per_pixel), 1)

        metrics["score"] = self._calculate_posture_score(metrics, "back_front")
        return metrics

    def _calculate_side_metrics(self, keypoints: Dict) -> Dict:
        metrics = {
            "ratio": self.ratio_mm_per_pixel,
            "head_shift": 0.0,
            "head_tilt": 0.0,
            "score": 0.0
        }

        if "nose" in keypoints and "left_shoulder" in keypoints:
            nose_pos = keypoints["nose"]["position"]
            shoulder_pos = keypoints["left_shoulder"]["position"]

            head_shift_pixels = abs(nose_pos[0] - shoulder_pos[0])
            metrics["head_shift"] = round(head_shift_pixels * self.ratio_mm_per_pixel, 1)

        if "nose" in keypoints and "left_ear" in keypoints:
            nose_pos = keypoints["nose"]["position"]
            ear_pos = keypoints["left_ear"]["position"]

            dx = ear_pos[0] - nose_pos[0]
            dy = ear_pos[1] - nose_pos[1]

            angle = math.degrees(math.atan2(dy, dx))
            metrics["head_tilt"] = round(abs(angle), 1)

        elif "nose" in keypoints and "right_ear" in keypoints:
            nose_pos = keypoints["nose"]["position"]
            ear_pos = keypoints["right_ear"]["position"]

            dx = ear_pos[0] - nose_pos[0]
            dy = ear_pos[1] - nose_pos[1]

            angle = math.degrees(math.atan2(dy, dx))
            metrics["head_tilt"] = round(abs(angle), 1)

        metrics["score"] = self._calculate_posture_score(metrics, "side")
        return metrics

    def _calculate_height_difference_and_angle(self, point1: Tuple[float, float],
                                               point2: Tuple[float, float]) -> Tuple[float, float]:
        x1, y1 = point1
        x2, y2 = point2

        height_diff = abs(y2 - y1)

        dx = x2 - x1
        dy = y2 - y1

        angle = math.degrees(math.atan2(dy, dx))

        return height_diff, angle

    def _calculate_spine_deviation(self, left_shoulder: Tuple[float, float],
                                   right_shoulder: Tuple[float, float],
                                   left_hip: Tuple[float, float],
                                   right_hip: Tuple[float, float]) -> float:
        shoulder_center_x = (left_shoulder[0] + right_shoulder[0]) / 2
        hip_center_x = (left_hip[0] + right_hip[0]) / 2

        deviation = abs(shoulder_center_x - hip_center_x)

        return deviation

    def _calculate_posture_score(self, metrics: Dict, analysis_type: str) -> float:
        score = 100.0

        if analysis_type == "back_front":
            if metrics["shoulder_imbalance"] > 5:
                score -= min(metrics["shoulder_imbalance"] * 2, 40)

            if metrics["hip_imbalance"] > 5:
                score -= min(metrics["hip_imbalance"] * 2, 30)

            if metrics["spine_deviation"] > 10:
                score -= min(metrics["spine_deviation"] * 1.5, 30)

        elif analysis_type == "side":
            if metrics["head_shift"] > 20:
                score -= min(metrics["head_shift"] * 1.5, 50)

            if metrics["head_tilt"] > 10:
                score -= min(metrics["head_tilt"] * 2, 50)

        score = max(0.0, score)

        return round(score, 1)

    def _empty_metrics(self) -> Dict:
        return {
            "ratio": 0.0,
            "shoulder_imbalance": 0.0,
            "hip_imbalance": 0.0,
            "spine_deviation": 0.0,
            "head_shift": 0.0,
            "head_tilt": 0.0,
            "score": 0.0
        }

    def generate_recommendations(self, classification: str, score: float) -> str:
        if score >= 80:
            return "Postur baik. Pertahankan dengan latihan rutin."
        elif score >= 60:
            return "Postur cukup baik. Perhatikan posisi duduk dan berdiri."
        elif score >= 40:
            return "Postur perlu perbaikan. Konsultasi dengan fisioterapis direkomendasikan."
        else:
            return "Postur kritis. Segera konsultasi dengan spesialis."

    def determine_analysis_type(self, classification: str) -> str:
        side_keywords = ["Kanan", "Kiri"]

        for keyword in side_keywords:
            if keyword in classification:
                return "side_analysis"

        return "back_front_analysis"
