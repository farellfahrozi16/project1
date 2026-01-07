import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

from src.dashboards.dashboard1 import Dashboard1
from src.dashboards.dashboard2 import Dashboard2
from src.dashboards.dashboard3 import Dashboard3
from src.dashboards.dashboard4 import Dashboard4
from src.analysis.yolo_analyzer import YOLOPostureAnalyzer
from src.analysis.posture_calculator import PostureCalculator
from src.utils.database import DatabaseManager

class PostureAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("KURO Performance - Postural Assessment")
        self.geometry("1400x900")
        self.configure(bg='black')

        self.user_name = ""
        self.user_height = 0.0
        self.uploaded_images = []
        self.model_path = None
        self.confidence_threshold = 0.25
        self.analysis_results = []

        self.db_manager = DatabaseManager()
        self.session_id = None

        self.container = tk.Frame(self, bg='black')
        self.container.pack(fill='both', expand=True)

        self.frames = {}

        for F in (Dashboard1, Dashboard2, Dashboard3, Dashboard4):
            frame = F(self.container, self)
            self.frames[F.__name__.lower()] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_dashboard("dashboard1")

    def show_dashboard(self, dashboard_name):
        frame = self.frames.get(dashboard_name)
        if frame:
            frame.tkraise()

            if dashboard_name == "dashboard3":
                self.after(100, lambda: self.frames["dashboard3"].display_results())
            elif dashboard_name == "dashboard4":
                self.after(100, lambda: self.frames["dashboard4"].display_detailed_results())

    def set_user_data(self, name: str, height: float):
        self.user_name = name
        self.user_height = height

        self.session_id = self.db_manager.save_user_session(name, height)

        print(f"User data set: {name}, {height} mm")
        if self.session_id:
            print(f"Session saved with ID: {self.session_id}")

    def set_analysis_params(self, images: list, model_path: str, confidence: float):
        self.uploaded_images = images
        self.model_path = model_path
        self.confidence_threshold = confidence

        print(f"Analysis params set: {len(images)} images, confidence: {confidence}")

    def run_analysis(self):
        if not self.uploaded_images or not self.model_path:
            raise ValueError("Missing images or model")

        print("Starting analysis...")

        try:
            analyzer = YOLOPostureAnalyzer(self.model_path)
            calculator = PostureCalculator(self.user_height)

            self.analysis_results = []

            for image_path in self.uploaded_images:
                print(f"Analyzing: {image_path}")

                analysis_data = analyzer.analyze_image(image_path, self.confidence_threshold)

                if analysis_data["detections"]:
                    detection = analysis_data["detections"][0]
                    classification = detection["classification"]
                    confidence = detection["confidence"]
                    keypoints = detection["keypoints"]

                    analysis_type = calculator.determine_analysis_type(classification)

                    metrics = calculator.calculate_posture_metrics(keypoints, analysis_type)

                    annotated_image = analyzer.annotate_image(image_path, analysis_data)

                    result = {
                        "image_path": image_path,
                        "classification": classification,
                        "confidence": confidence,
                        "analysis_type": analysis_type,
                        "metrics": metrics,
                        "score": metrics.get("score", 0.0),
                        "analysis_data": analysis_data,
                        "annotated_image": annotated_image
                    }

                    self.analysis_results.append(result)

                    if self.session_id:
                        self.db_manager.save_analysis_result(self.session_id, {
                            "analysis_type": analysis_type,
                            "classification": classification,
                            "confidence": confidence,
                            "score": metrics.get("score", 0.0),
                            "measurements": metrics,
                            "keypoints": keypoints
                        })

                    print(f"Analysis complete: {classification} (Confidence: {confidence:.2%})")

            print(f"Total results: {len(self.analysis_results)}")

        except Exception as e:
            print(f"Analysis error: {e}")
            raise

def main():
    try:
        app = PostureAnalysisApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
