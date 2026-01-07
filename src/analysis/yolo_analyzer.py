import cv2
import numpy as np
from ultralytics import YOLO
from typing import Dict, List, Tuple, Optional
import time
from src.config import KEYPOINT_NAMES, CONFIDENCE_LEVELS, POSTURE_CLASSIFICATION_MAP

class YOLOPostureAnalyzer:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.model_path = model_path

    def analyze_image(self, image_path: str, confidence_threshold: float = 0.25) -> Dict:
        start_time = time.time()

        results = self.model(image_path, conf=confidence_threshold)

        analysis_data = {
            "image_path": image_path,
            "detections": [],
            "total_detections": 0,
            "classifications": {},
            "processing_time": 0
        }

        for result in results:
            if result.boxes is not None:
                for idx, box in enumerate(result.boxes):
                    detection = self._process_detection(box, result, idx)
                    analysis_data["detections"].append(detection)

                    classification = detection["classification"]
                    if classification not in analysis_data["classifications"]:
                        analysis_data["classifications"][classification] = 0
                    analysis_data["classifications"][classification] += 1

        analysis_data["total_detections"] = len(analysis_data["detections"])
        analysis_data["processing_time"] = round(time.time() - start_time, 2)

        return analysis_data

    def _process_detection(self, box, result, idx: int) -> Dict:
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        class_name = result.names[cls]

        classification = POSTURE_CLASSIFICATION_MAP.get(class_name, class_name)

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        width = x2 - x1
        height = y2 - y1
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        area = width * height

        conf_level = self._get_confidence_level(conf)

        detection = {
            "index": idx + 1,
            "class": class_name,
            "classification": classification,
            "sub_category": class_name,
            "confidence": conf,
            "confidence_percent": round(conf * 100, 1),
            "confidence_level": conf_level,
            "bbox": [float(x1), float(y1), float(x2), float(y2)],
            "width": float(width),
            "height": float(height),
            "center": (float(center_x), float(center_y)),
            "area": float(area),
            "keypoints": {}
        }

        if hasattr(result, 'keypoints') and result.keypoints is not None:
            detection["keypoints"] = self._extract_keypoints(result.keypoints, idx)

        return detection

    def _extract_keypoints(self, keypoints_data, detection_idx: int) -> Dict:
        keypoints = {}

        if keypoints_data.xy is not None and len(keypoints_data.xy) > detection_idx:
            kpts_xy = keypoints_data.xy[detection_idx].cpu().numpy()
            kpts_conf = keypoints_data.conf[detection_idx].cpu().numpy() if keypoints_data.conf is not None else None

            for kpt_idx, (x, y) in enumerate(kpts_xy):
                if kpt_idx in KEYPOINT_NAMES:
                    kpt_name = KEYPOINT_NAMES[kpt_idx]
                    confidence = float(kpts_conf[kpt_idx]) if kpts_conf is not None else 0.0

                    if confidence > 0.0:
                        keypoints[kpt_name] = {
                            "position": (float(x), float(y)),
                            "confidence": confidence,
                            "confidence_level": self._get_confidence_level(confidence)
                        }

        return keypoints

    def _get_confidence_level(self, conf: float) -> str:
        for (min_val, max_val), level in CONFIDENCE_LEVELS.items():
            if min_val <= conf < max_val:
                return level
        return "Unknown"

    def annotate_image(self, image_path: str, analysis_data: Dict) -> np.ndarray:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        for detection in analysis_data["detections"]:
            x1, y1, x2, y2 = detection["bbox"]

            color = self._get_classification_color(detection["classification"])

            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)

            label = f"{detection['classification']}: {detection['confidence_percent']}%"
            (label_w, label_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(image, (int(x1), int(y1) - label_h - 10),
                         (int(x1) + label_w, int(y1)), color, -1)
            cv2.putText(image, label, (int(x1), int(y1) - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if detection["keypoints"]:
                self._draw_keypoints(image, detection["keypoints"])

        return image

    def _draw_keypoints(self, image: np.ndarray, keypoints: Dict):
        skeleton = [
            ("left_shoulder", "right_shoulder"),
            ("left_shoulder", "left_elbow"),
            ("left_elbow", "left_wrist"),
            ("right_shoulder", "right_elbow"),
            ("right_elbow", "right_wrist"),
            ("left_shoulder", "left_hip"),
            ("right_shoulder", "right_hip"),
            ("left_hip", "right_hip"),
            ("left_hip", "left_knee"),
            ("left_knee", "left_ankle"),
            ("right_hip", "right_knee"),
            ("right_knee", "right_ankle"),
            ("nose", "left_eye"),
            ("nose", "right_eye"),
            ("left_eye", "left_ear"),
            ("right_eye", "right_ear")
        ]

        for kpt_name, kpt_data in keypoints.items():
            x, y = kpt_data["position"]
            conf = kpt_data["confidence"]

            if conf > 0.3:
                cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
                cv2.circle(image, (int(x), int(y)), 7, (255, 255, 255), 2)

        for kpt1_name, kpt2_name in skeleton:
            if kpt1_name in keypoints and kpt2_name in keypoints:
                conf1 = keypoints[kpt1_name]["confidence"]
                conf2 = keypoints[kpt2_name]["confidence"]

                if conf1 > 0.3 and conf2 > 0.3:
                    x1, y1 = keypoints[kpt1_name]["position"]
                    x2, y2 = keypoints[kpt2_name]["position"]
                    cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

    def _get_classification_color(self, classification: str) -> Tuple[int, int, int]:
        colors = {
            "Normal": (0, 255, 0),
            "Kyphosis": (0, 0, 255),
            "Lordosis": (255, 0, 0),
            "Swayback": (255, 165, 0)
        }
        return colors.get(classification, (128, 128, 128))
