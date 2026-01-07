import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

class Dashboard1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='black')
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        main_container = tk.Frame(self, bg='black')
        main_container.pack(expand=True, fill='both')

        left_frame = tk.Frame(main_container, bg='black')
        left_frame.pack(side='left', expand=True, fill='both', padx=50, pady=50)

        try:
            logo_path = Path(__file__).parent.parent.parent / "assets" / "kuro_logo.png"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((400, 400), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            logo_label = tk.Label(left_frame, image=self.logo_photo, bg='black')
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = tk.Label(left_frame, text="KURO\nPERFORMANCE",
                                 font=('Arial', 36, 'bold'), fg='#3FB5E5', bg='black')
            logo_label.pack(pady=20)

        right_frame = tk.Frame(main_container, bg='black')
        right_frame.pack(side='right', expand=True, fill='both', padx=50, pady=50)

        title_label = tk.Label(right_frame, text="POSTURAL ASSESSMENT",
                              font=('Arial', 28, 'bold'), fg='white', bg='black')
        title_label.pack(pady=(50, 30))

        form_container = tk.Frame(right_frame, bg='#E8EAF6', bd=2, relief='flat')
        form_container.pack(pady=20, padx=100, fill='both', expand=True)

        form_inner = tk.Frame(form_container, bg='#E8EAF6')
        form_inner.pack(expand=True, pady=40, padx=40)

        name_label = tk.Label(form_inner, text="Name", font=('Arial', 14),
                             bg='#E8EAF6', fg='black', anchor='w')
        name_label.pack(fill='x', pady=(10, 5))

        self.name_entry = tk.Entry(form_inner, font=('Arial', 14), bg='white',
                                   relief='solid', bd=1)
        self.name_entry.pack(fill='x', pady=(0, 20), ipady=8)

        height_label = tk.Label(form_inner, text="Height", font=('Arial', 14),
                               bg='#E8EAF6', fg='black', anchor='w')
        height_label.pack(fill='x', pady=(10, 5))

        self.height_entry = tk.Entry(form_inner, font=('Arial', 14), bg='white',
                                     relief='solid', bd=1)
        self.height_entry.pack(fill='x', pady=(0, 20), ipady=8)

        button_frame = tk.Frame(form_inner, bg='#E8EAF6')
        button_frame.pack(pady=20)

        submit_button = tk.Button(button_frame, text="Mulai Analisis",
                                 font=('Arial', 14, 'bold'),
                                 bg='#3FB5E5', fg='white',
                                 relief='flat', bd=0,
                                 padx=40, pady=12,
                                 cursor='hand2',
                                 command=self.submit_form)
        submit_button.pack()

    def submit_form(self):
        name = self.name_entry.get().strip()
        height = self.height_entry.get().strip()

        if not name:
            tk.messagebox.showerror("Error", "Nama tidak boleh kosong!")
            return

        try:
            height_value = float(height)
            if height_value <= 0:
                raise ValueError("Height must be positive")
        except ValueError:
            tk.messagebox.showerror("Error", "Tinggi harus berupa angka positif!")
            return

        self.controller.set_user_data(name, height_value)

        self.controller.show_dashboard("dashboard2")
