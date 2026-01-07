import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import threading

class Dashboard2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller

        self.uploaded_images = []
        self.model_path = None
        self.confidence_threshold = 0.25

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

        title_label = tk.Label(header_frame, text="POSTURAL ASSESSMENT",
                              font=('Arial', 24, 'bold'), fg='white', bg='black')
        title_label.pack(side='left', padx=10)

        content_frame = tk.Frame(self, bg='black')
        content_frame.pack(expand=True, fill='both', padx=20, pady=10)

        top_section = tk.Frame(content_frame, bg='#1E1E1E', relief='solid', bd=1)
        top_section.pack(fill='x', pady=(0, 10))

        upload_label = tk.Label(top_section, text="Upload Image",
                               font=('Arial', 14), bg='white', fg='black',
                               relief='flat', padx=20, pady=10)
        upload_label.pack(side='left', padx=10, pady=10)

        upload_button = tk.Button(top_section, text="Browse Images",
                                 font=('Arial', 12), bg='#3FB5E5', fg='white',
                                 relief='flat', padx=20, pady=8,
                                 cursor='hand2',
                                 command=self.upload_images)
        upload_button.pack(side='left', padx=10)

        self.image_count_label = tk.Label(top_section, text="0 images selected",
                                         font=('Arial', 12), fg='white', bg='#1E1E1E')
        self.image_count_label.pack(side='left', padx=20)

        menu_frame = tk.Frame(top_section, bg='white', relief='flat')
        menu_frame.pack(side='right', padx=10, pady=10)

        menu_label = tk.Label(menu_frame, text="Menu:",
                             font=('Arial', 12, 'bold'), bg='white', fg='black')
        menu_label.pack(side='left', padx=5)

        menu_buttons = [
            ("1. Analisis Single", self.analyze_single),
            ("2. Analisis Batch", self.analyze_batch),
            ("3. System Info", self.show_system_info),
            ("4. Keluar", self.exit_app)
        ]

        for text, command in menu_buttons:
            btn = tk.Button(menu_frame, text=text,
                          font=('Arial', 10), bg='#E8EAF6', fg='black',
                          relief='flat', padx=10, pady=5,
                          cursor='hand2',
                          command=command)
            btn.pack(side='left', padx=2)

        controls_frame = tk.Frame(content_frame, bg='#1E1E1E', relief='solid', bd=1)
        controls_frame.pack(fill='x', pady=(0, 10))

        model_section = tk.Frame(controls_frame, bg='#1E1E1E')
        model_section.pack(fill='x', padx=20, pady=10)

        model_label = tk.Label(model_section, text="Upload Model YOLO (.pt):",
                              font=('Arial', 12, 'bold'), fg='white', bg='#1E1E1E')
        model_label.pack(side='left', padx=(0, 10))

        model_button = tk.Button(model_section, text="Browse Model",
                                font=('Arial', 11), bg='#4CAF50', fg='white',
                                relief='flat', padx=20, pady=8,
                                cursor='hand2',
                                command=self.upload_model)
        model_button.pack(side='left', padx=10)

        self.model_status_label = tk.Label(model_section, text="No model loaded",
                                          font=('Arial', 11), fg='#FF5252', bg='#1E1E1E')
        self.model_status_label.pack(side='left', padx=10)

        confidence_section = tk.Frame(controls_frame, bg='#1E1E1E')
        confidence_section.pack(fill='x', padx=20, pady=10)

        conf_label = tk.Label(confidence_section, text="Confidence Threshold:",
                            font=('Arial', 12, 'bold'), fg='white', bg='#1E1E1E')
        conf_label.pack(side='left', padx=(0, 10))

        self.confidence_var = tk.DoubleVar(value=0.25)
        self.confidence_scale = tk.Scale(confidence_section, from_=0.0, to=1.0,
                                        resolution=0.05, orient='horizontal',
                                        variable=self.confidence_var,
                                        bg='#1E1E1E', fg='white',
                                        highlightthickness=0,
                                        length=300)
        self.confidence_scale.pack(side='left', padx=10)

        self.confidence_value_label = tk.Label(confidence_section, text="0.25",
                                              font=('Arial', 11, 'bold'),
                                              fg='#3FB5E5', bg='#1E1E1E')
        self.confidence_value_label.pack(side='left', padx=10)

        self.confidence_var.trace_add('write', self.update_confidence_label)

        analyze_button = tk.Button(controls_frame, text="ANALYZE IMAGES",
                                  font=('Arial', 14, 'bold'), bg='#FF5252', fg='white',
                                  relief='flat', padx=40, pady=15,
                                  cursor='hand2',
                                  command=self.start_analysis)
        analyze_button.pack(pady=20)

        preview_frame = tk.Frame(content_frame, bg='#1E1E1E', relief='solid', bd=1)
        preview_frame.pack(expand=True, fill='both')

        preview_label = tk.Label(preview_frame, text="Image Preview",
                                font=('Arial', 14, 'bold'), fg='white', bg='#1E1E1E')
        preview_label.pack(pady=10)

        self.preview_canvas = tk.Canvas(preview_frame, bg='#2E2E2E',
                                       highlightthickness=0)
        self.preview_canvas.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = tk.Scrollbar(preview_frame, orient='vertical',
                                command=self.preview_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.preview_canvas.configure(yscrollcommand=scrollbar.set)

        self.preview_inner_frame = tk.Frame(self.preview_canvas, bg='#2E2E2E')
        self.preview_canvas.create_window((0, 0), window=self.preview_inner_frame, anchor='nw')

        self.preview_inner_frame.bind('<Configure>',
                                     lambda e: self.preview_canvas.configure(
                                         scrollregion=self.preview_canvas.bbox('all')))

    def update_confidence_label(self, *args):
        value = self.confidence_var.get()
        self.confidence_value_label.config(text=f"{value:.2f}")
        self.confidence_threshold = value

    def upload_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )

        if files:
            self.uploaded_images = list(files)
            self.image_count_label.config(text=f"{len(self.uploaded_images)} images selected")
            self.display_image_previews()

    def display_image_previews(self):
        for widget in self.preview_inner_frame.winfo_children():
            widget.destroy()

        self.preview_photos = []

        for idx, img_path in enumerate(self.uploaded_images):
            try:
                img = Image.open(img_path)
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_photos.append(photo)

                img_label = tk.Label(self.preview_inner_frame, image=photo, bg='#2E2E2E')
                img_label.grid(row=idx // 4, column=idx % 4, padx=10, pady=10)

                name_label = tk.Label(self.preview_inner_frame,
                                    text=Path(img_path).name,
                                    font=('Arial', 9), fg='white', bg='#2E2E2E')
                name_label.grid(row=idx // 4 + 1, column=idx % 4)
            except Exception as e:
                print(f"Error loading preview for {img_path}: {e}")

    def upload_model(self):
        file = filedialog.askopenfilename(
            title="Select YOLO Model",
            filetypes=[("PyTorch Model", "*.pt"), ("All files", "*.*")]
        )

        if file:
            self.model_path = file
            model_name = Path(file).name
            self.model_status_label.config(text=f"Model: {model_name}", fg='#4CAF50')

    def analyze_single(self):
        messagebox.showinfo("Info", "Mode: Analisis Single Image")

    def analyze_batch(self):
        messagebox.showinfo("Info", "Mode: Analisis Batch Images")

    def show_system_info(self):
        info = f"User: {self.controller.user_name}\n"
        info += f"Height: {self.controller.user_height} mm\n"
        info += f"Images: {len(self.uploaded_images)}\n"
        info += f"Model: {Path(self.model_path).name if self.model_path else 'None'}\n"
        info += f"Confidence: {self.confidence_threshold}"

        messagebox.showinfo("System Info", info)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Apakah Anda yakin ingin keluar?"):
            self.controller.quit()

    def start_analysis(self):
        if not self.uploaded_images:
            messagebox.showerror("Error", "Silakan upload gambar terlebih dahulu!")
            return

        if not self.model_path:
            messagebox.showerror("Error", "Silakan upload model YOLO terlebih dahulu!")
            return

        self.controller.set_analysis_params(
            images=self.uploaded_images,
            model_path=self.model_path,
            confidence=self.confidence_threshold
        )

        progress_window = tk.Toplevel(self)
        progress_window.title("Processing")
        progress_window.geometry("400x150")
        progress_window.configure(bg='#1E1E1E')

        label = tk.Label(progress_window, text="Analyzing images...",
                        font=('Arial', 14), fg='white', bg='#1E1E1E')
        label.pack(pady=20)

        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=300)
        progress_bar.pack(pady=20)
        progress_bar.start()

        def process():
            try:
                self.controller.run_analysis()
                progress_window.destroy()
                self.controller.show_dashboard("dashboard3")
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")

        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
