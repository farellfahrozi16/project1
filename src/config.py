import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
MODELS_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"

MODELS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

LOGO_PATH = ASSETS_DIR / "kuro_logo.png"
ICON_PATH = ASSETS_DIR / "kuro_rebranding_icon_full_clr_online.png"

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

POSTURE_CLASSIFICATION_MAP = {
    "Normal-Kanan": "Normal",
    "Normal-Kiri": "Normal",
    "Normal-Belakang": "Normal",
    "Normal-Depan": "Normal",
    "Kyphosis-Kanan": "Kyphosis",
    "Kyphosis-Kiri": "Kyphosis",
    "Kyphosis-Belakang": "Kyphosis",
    "Kyphosis-Depan": "Kyphosis",
    "Lordosis-Kanan": "Lordosis",
    "Lordosis-Kiri": "Lordosis",
    "Lordosis-Belakang": "Lordosis",
    "Lordosis-Depan": "Lordosis",
    "Swayback-Kanan": "Swayback",
    "Swayback-Kiri": "Swayback",
    "Swayback-Belakang": "Swayback",
    "Swayback-Depan": "Swayback",
}

CONFIDENCE_LEVELS = {
    (0.9, 1.0): "Sangat Tinggi",
    (0.7, 0.9): "Tinggi",
    (0.5, 0.7): "Sedang",
    (0.3, 0.5): "Rendah",
    (0.0, 0.3): "Sangat Rendah"
}

KEYPOINT_NAMES = {
    0: "nose",
    1: "left_eye",
    2: "right_eye",
    3: "left_ear",
    4: "right_ear",
    5: "left_shoulder",
    6: "right_shoulder",
    7: "left_elbow",
    8: "right_elbow",
    9: "left_wrist",
    10: "right_wrist",
    11: "left_hip",
    12: "right_hip",
    13: "left_knee",
    14: "right_knee",
    15: "left_ankle",
    16: "right_ankle"
}

KEYPOINT_EMOJIS = {
    "nose": "👃",
    "left_eye": "👁️",
    "right_eye": "👁️",
    "left_ear": "👂",
    "right_ear": "👂",
    "left_shoulder": "💪",
    "right_shoulder": "💪",
    "left_elbow": "🦾",
    "right_elbow": "🦾",
    "left_wrist": "🤲",
    "right_wrist": "🤲",
    "left_hip": "🦵",
    "right_hip": "🦵",
    "left_knee": "🦿",
    "right_knee": "🦿",
    "left_ankle": "🦶",
    "right_ankle": "🦶"
}
