from supabase import create_client, Client
from datetime import datetime
import json
from src.config import SUPABASE_URL, SUPABASE_KEY

class DatabaseManager:
    def __init__(self):
        if SUPABASE_URL and SUPABASE_KEY:
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.connected = True
        else:
            self.client = None
            self.connected = False
            print("Warning: Supabase credentials not found. Database features disabled.")

    def save_user_session(self, name: str, height: float):
        if not self.connected:
            return None

        try:
            data = {
                "name": name,
                "height": height,
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("user_sessions").insert(data).execute()
            return result.data[0]["id"] if result.data else None
        except Exception as e:
            print(f"Error saving user session: {e}")
            return None

    def save_analysis_result(self, session_id: str, analysis_data: dict):
        if not self.connected:
            return None

        try:
            data = {
                "session_id": session_id,
                "analysis_type": analysis_data.get("analysis_type"),
                "classification": analysis_data.get("classification"),
                "confidence": analysis_data.get("confidence"),
                "score": analysis_data.get("score"),
                "measurements": json.dumps(analysis_data.get("measurements", {})),
                "keypoints": json.dumps(analysis_data.get("keypoints", {})),
                "created_at": datetime.now().isoformat()
            }
            result = self.client.table("analysis_results").insert(data).execute()
            return result.data[0]["id"] if result.data else None
        except Exception as e:
            print(f"Error saving analysis result: {e}")
            return None

    def get_session_results(self, session_id: str):
        if not self.connected:
            return []

        try:
            result = self.client.table("analysis_results").select("*").eq("session_id", session_id).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching session results: {e}")
            return []
