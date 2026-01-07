import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.utils.visualization import PostureVisualizer
from src.utils.export import ResultExporter

class Dashboard4(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#E8EAF6')
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

        title_label = tk.Label(header_frame, text="POSTURAL ASSESSMENT - Detailed Report",
                              font=('Arial', 24, 'bold'), fg='white', bg='black')
        title_label.pack(side='left', padx=10)

        main_scroll = tk.Canvas(self, bg='#E8EAF6', highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient='vertical', command=main_scroll.yview)

        main_scroll.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        main_scroll.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame = tk.Frame(main_scroll, bg='#E8EAF6')
        main_scroll.create_window((0, 0), window=self.scroll_frame, anchor='nw')

        self.scroll_frame.bind('<Configure>',
                              lambda e: main_scroll.configure(scrollregion=main_scroll.bbox('all')))

        self.image_frame = tk.Frame(self.scroll_frame, bg='white', relief='solid', bd=2)
        self.image_frame.pack(fill='x', padx=20, pady=10)

        image_title = tk.Label(self.image_frame, text="ANALYZED IMAGE WITH ANNOTATIONS",
                              font=('Arial', 14, 'bold'), bg='white', fg='black')
        image_title.pack(pady=10)

        self.image_canvas = tk.Canvas(self.image_frame, bg='#F5F5F5',
                                     height=400, highlightthickness=0)
        self.image_canvas.pack(fill='x', padx=10, pady=10)

        self.graphs_frame = tk.Frame(self.scroll_frame, bg='white', relief='solid', bd=2)
        self.graphs_frame.pack(fill='x', padx=20, pady=10)

        graphs_title = tk.Label(self.graphs_frame, text="VISUALIZATION CHARTS",
                               font=('Arial', 14, 'bold'), bg='white', fg='black')
        graphs_title.pack(pady=10)

        self.graphs_container = tk.Frame(self.graphs_frame, bg='white')
        self.graphs_container.pack(fill='both', padx=10, pady=10)

        table_frame = tk.Frame(self.scroll_frame, bg='white', relief='solid', bd=2)
        table_frame.pack(fill='x', padx=20, pady=10)

        table_title = tk.Label(table_frame, text="TABEL HASIL ANALISIS IMBALANCE POSTURAL",
                              font=('Arial', 14, 'bold'), bg='white', fg='black')
        table_title.pack(pady=10)

        self.table_container = tk.Frame(table_frame, bg='white')
        self.table_container.pack(fill='x', padx=20, pady=10)

        export_button = tk.Button(table_frame, text="Export to CSV",
                                 font=('Arial', 12, 'bold'),
                                 bg='#4CAF50', fg='white',
                                 relief='flat', padx=30, pady=10,
                                 cursor='hand2',
                                 command=self.export_csv)
        export_button.pack(pady=10)

        report_frame = tk.Frame(self.scroll_frame, bg='#1E1E1E', relief='solid', bd=2)
        report_frame.pack(fill='x', padx=20, pady=10)

        report_title = tk.Label(report_frame, text="LAPORAN ANALISIS",
                               font=('Arial', 14, 'bold'), fg='white', bg='#1E1E1E')
        report_title.pack(pady=10)

        self.report_text = tk.Text(report_frame, height=12, font=('Courier', 11),
                                  bg='#2E2E2E', fg='white',
                                  relief='flat', padx=20, pady=10,
                                  wrap='word')
        self.report_text.pack(fill='x', padx=20, pady=10)

        button_frame = tk.Frame(self.scroll_frame, bg='#E8EAF6')
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back to Analysis",
                               font=('Arial', 14, 'bold'),
                               bg='#757575', fg='white',
                               relief='flat', padx=40, pady=15,
                               cursor='hand2',
                               command=self.back_to_analysis)
        back_button.pack(side='left', padx=10)

        menu_button = tk.Button(button_frame, text="Back to Menu",
                               font=('Arial', 14, 'bold'),
                               bg='#3FB5E5', fg='white',
                               relief='flat', padx=40, pady=15,
                               cursor='hand2',
                               command=self.back_to_menu)
        menu_button.pack(side='left', padx=10)

    def display_detailed_results(self):
        analysis_results = self.controller.analysis_results

        if not analysis_results:
            return

        result = analysis_results[0]

        self.display_annotated_image(result['annotated_image'])

        self.display_graphs(result['metrics'], result['analysis_type'])

        self.display_table(result['metrics'], result['analysis_type'])

        self.display_report(result)

    def display_annotated_image(self, image_array):
        try:
            img_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil.thumbnail((800, 400), Image.Resampling.LANCZOS)
            self.annotated_photo = ImageTk.PhotoImage(img_pil)

            self.image_canvas.delete('all')
            self.image_canvas.create_image(400, 200, image=self.annotated_photo, anchor='center')
        except Exception as e:
            print(f"Error displaying annotated image: {e}")

    def display_graphs(self, metrics, analysis_type):
        for widget in self.graphs_container.winfo_children():
            widget.destroy()

        visualizer = PostureVisualizer()

        if analysis_type == "back_front_analysis":
            shoulder_fig = visualizer.create_shoulder_plot(metrics.get('shoulder_imbalance', 0.0))
            shoulder_canvas = FigureCanvasTkAgg(shoulder_fig, self.graphs_container)
            shoulder_canvas.draw()
            shoulder_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

            hip_fig = visualizer.create_hip_plot(metrics.get('hip_imbalance', 0.0))
            hip_canvas = FigureCanvasTkAgg(hip_fig, self.graphs_container)
            hip_canvas.draw()
            hip_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

            spine_fig = visualizer.create_spine_plot(metrics.get('spine_deviation', 0.0))
            spine_canvas = FigureCanvasTkAgg(spine_fig, self.graphs_container)
            spine_canvas.draw()
            spine_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

            scapular_fig = visualizer.create_scapular_plot(118.6)
            scapular_canvas = FigureCanvasTkAgg(scapular_fig, self.graphs_container)
            scapular_canvas.draw()
            scapular_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10)

        elif analysis_type == "side_analysis":
            head_fig = visualizer.create_head_tilt_plot(metrics.get('head_tilt', 0.0))
            head_canvas = FigureCanvasTkAgg(head_fig, self.graphs_container)
            head_canvas.draw()
            head_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

            foot_fig = visualizer.create_foot_plot()
            foot_canvas = FigureCanvasTkAgg(foot_fig, self.graphs_container)
            foot_canvas.draw()
            foot_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

    def display_table(self, metrics, analysis_type):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        exporter = ResultExporter()
        df = exporter.create_analysis_table(metrics, analysis_type)

        self.current_df = df

        tree = ttk.Treeview(self.table_container, columns=list(df.columns),
                           show='headings', height=10)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')

        for _, row in df.iterrows():
            tree.insert('', 'end', values=list(row))

        tree.pack(fill='x', padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.table_container, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

    def display_report(self, result):
        self.report_text.delete('1.0', tk.END)

        report = "=" * 60 + "\n"
        report += "HASIL KLASIFIKASI POSTURAL:\n"
        report += "=" * 60 + "\n\n"

        classifications = result['analysis_data']['classifications']
        for classification, count in classifications.items():
            report += f"🦴 {classification}: {count} deteksi\n"

        report += "\n" + "=" * 60 + "\n"
        report += "💡 REKOMENDASI BERDASARKAN ANALISIS:\n"
        report += "=" * 60 + "\n"

        exporter = ResultExporter()
        recommendation = exporter.format_recommendation(result['classification'], result['score'])
        report += recommendation + "\n"

        report += "\n" + "=" * 60 + "\n"
        report += "DETAIL PENGUKURAN:\n"
        report += "=" * 60 + "\n"

        metrics = result['metrics']
        if 'shoulder_imbalance' in metrics:
            report += f"   Shoulder Imbalance: {metrics['shoulder_imbalance']:.1f} mm\n"
        if 'hip_imbalance' in metrics:
            report += f"   Hip Imbalance: {metrics['hip_imbalance']:.1f} mm\n"
        if 'spine_deviation' in metrics:
            report += f"   Spine Deviation: {metrics['spine_deviation']:.1f} mm\n"
        if 'head_shift' in metrics:
            report += f"   Head Shift: {metrics['head_shift']:.1f} mm\n"
        if 'head_tilt' in metrics:
            report += f"   Head Tilt: {metrics['head_tilt']:.1f}°\n"

        report += f"\n   Posture Score: {result['score']:.1f}/100\n"
        report += f"   Rasio: {metrics.get('ratio', 0.0):.6f} mm/pixel\n"

        self.report_text.insert('1.0', report)

    def export_csv(self):
        if not hasattr(self, 'current_df'):
            messagebox.showwarning("Warning", "No data to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="posture_analysis_report.csv"
        )

        if file_path:
            try:
                exporter = ResultExporter()
                exporter.export_to_csv(self.current_df, file_path)
                messagebox.showinfo("Success", f"Report exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def back_to_analysis(self):
        self.controller.show_dashboard("dashboard3")

    def back_to_menu(self):
        self.controller.show_dashboard("dashboard2")
