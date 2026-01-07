import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import cv2

class Dashboard3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self, bg='black', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)

        try:
            icon_path = Path(__file__).parent.parent.parent / "assets" / "kuro_rebranding_icon_full_clr_online.png"
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((60, 60), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)

            icon_label = tk.Label(header_frame, image=self.icon_photo, bg='black')
            icon_label.pack(side='left', padx=20, pady=10)
        except Exception as e:
            print(f"Error loading icon: {e}")

        title_label = tk.Label(header_frame, text="POSTURAL ASSESSMENT - Analysis Results",
                              font=('Arial', 24, 'bold'), fg='white', bg='black')
        title_label.pack(side='left', padx=10)

        content_frame = tk.Frame(self, bg='#E8EAF6')
        content_frame.pack(expand=True, fill='both', padx=20, pady=10)

        comparison_frame = tk.Frame(content_frame, bg='#E8EAF6')
        comparison_frame.pack(expand=True, fill='both', pady=10)

        self.before_frame = tk.Frame(comparison_frame, bg='white', relief='solid', bd=2)
        self.before_frame.pack(side='left', expand=True, fill='both', padx=10, pady=10)

        before_label = tk.Label(self.before_frame, text="BEFORE ANALYSIS",
                               font=('Arial', 14, 'bold'), bg='white', fg='black')
        before_label.pack(pady=10)

        self.before_canvas = tk.Canvas(self.before_frame, bg='#F5F5F5',
                                      highlightthickness=0)
        self.before_canvas.pack(expand=True, fill='both', padx=10, pady=10)

        self.after_frame = tk.Frame(comparison_frame, bg='white', relief='solid', bd=2)
        self.after_frame.pack(side='right', expand=True, fill='both', padx=10, pady=10)

        after_label = tk.Label(self.after_frame, text="AFTER ANALYSIS",
                              font=('Arial', 14, 'bold'), bg='white', fg='black')
        after_label.pack(pady=10)

        self.after_canvas = tk.Canvas(self.after_frame, bg='#F5F5F5',
                                     highlightthickness=0)
        self.after_canvas.pack(expand=True, fill='both', padx=10, pady=10)

        summary_frame = tk.Frame(content_frame, bg='#1E1E1E', relief='solid', bd=2)
        summary_frame.pack(fill='x', padx=10, pady=10)

        summary_title = tk.Label(summary_frame, text="HASIL ANALISIS SINGKAT",
                                font=('Arial', 14, 'bold'), fg='white', bg='#1E1E1E')
        summary_title.pack(pady=10)

        self.summary_text = tk.Text(summary_frame, height=6, font=('Courier', 11),
                                   bg='#2E2E2E', fg='white',
                                   relief='flat', padx=20, pady=10)
        self.summary_text.pack(fill='x', padx=20, pady=10)

        button_frame = tk.Frame(content_frame, bg='#E8EAF6')
        button_frame.pack(pady=20)

        results_button = tk.Button(button_frame, text="View Detailed Results",
                                  font=('Arial', 14, 'bold'),
                                  bg='#3FB5E5', fg='white',
                                  relief='flat', padx=40, pady=15,
                                  cursor='hand2',
                                  command=self.show_detailed_results)
        results_button.pack(side='left', padx=10)

        back_button = tk.Button(button_frame, text="Back to Menu",
                               font=('Arial', 14, 'bold'),
                               bg='#757575', fg='white',
                               relief='flat', padx=40, pady=15,
                               cursor='hand2',
                               command=self.back_to_menu)
        back_button.pack(side='left', padx=10)

    def display_results(self):
        analysis_results = self.controller.analysis_results

        if not analysis_results:
            return

        result = analysis_results[0]

        self.display_before_image(result['image_path'])

        if result['annotated_image'] is not None:
            self.display_after_image(result['annotated_image'])

        self.display_summary(result)

    def display_before_image(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((600, 600), Image.Resampling.LANCZOS)
            self.before_photo = ImageTk.PhotoImage(img)

            self.before_canvas.delete('all')
            canvas_width = self.before_canvas.winfo_width()
            canvas_height = self.before_canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                x = canvas_width // 2
                y = canvas_height // 2
                self.before_canvas.create_image(x, y, image=self.before_photo, anchor='center')
        except Exception as e:
            print(f"Error displaying before image: {e}")

    def display_after_image(self, image_array):
        try:
            img_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((600, 600), Image.Resampling.LANCZOS)
            self.after_photo = ImageTk.PhotoImage(img_pil)

            self.after_canvas.delete('all')
            canvas_width = self.after_canvas.winfo_width()
            canvas_height = self.after_canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                x = canvas_width // 2
                y = canvas_height // 2
                self.after_canvas.create_image(x, y, image=self.after_photo, anchor='center')
        except Exception as e:
            print(f"Error displaying after image: {e}")

    def display_summary(self, result):
        self.summary_text.delete('1.0', tk.END)

        summary = f"Classification: {result['classification']}\n"
        summary += f"Confidence: {result['confidence']:.2%}\n"
        summary += f"Score: {result['score']:.1f}/100\n"
        summary += f"\nKey Measurements:\n"

        metrics = result['metrics']
        if 'shoulder_imbalance' in metrics:
            summary += f"  Shoulder Imbalance: {metrics['shoulder_imbalance']:.1f} mm\n"
        if 'hip_imbalance' in metrics:
            summary += f"  Hip Imbalance: {metrics['hip_imbalance']:.1f} mm\n"
        if 'spine_deviation' in metrics:
            summary += f"  Spine Deviation: {metrics['spine_deviation']:.1f} mm\n"
        if 'head_shift' in metrics:
            summary += f"  Head Shift: {metrics['head_shift']:.1f} mm\n"
        if 'head_tilt' in metrics:
            summary += f"  Head Tilt: {metrics['head_tilt']:.1f}°\n"

        self.summary_text.insert('1.0', summary)

    def show_detailed_results(self):
        self.controller.show_dashboard("dashboard4")

    def back_to_menu(self):
        self.controller.show_dashboard("dashboard2")
