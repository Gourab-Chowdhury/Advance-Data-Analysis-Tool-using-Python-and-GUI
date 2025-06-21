import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class DataManager:
    def __init__(self, app):
        self.app = app
        self.data = None
    
    def setup_ui(self, parent):
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        # Set theme and define a bold, larger font style for the header
        style = ttk.Style()
        style.theme_use('clam')  # or 'default'
        style.configure('Header.TLabel', font=('Arial', 22, 'bold'))

        ttk.Label(header_frame, text="Data Loading & Exploration", style='Header.TLabel').pack()
        
        # File Loading
        file_frame = ttk.LabelFrame(parent, text="Data Import")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Load CSV", command=lambda: self.load_data('csv')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Load Excel", command=lambda: self.load_data('excel')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Load JSON", command=lambda: self.load_data('json')).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Data Display
        display_frame = ttk.Frame(parent)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.data_text = scrolledtext.ScrolledText(
            display_frame, wrap=tk.NONE, width=120, height=25
        )
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Data Info
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="No data loaded")
        self.info_label.pack(side=tk.LEFT)
        
        self.export_btn = ttk.Button(info_frame, text="Export Data", command=self.export_data, state='disabled')
        self.export_btn.pack(side=tk.RIGHT)
    
    def load_data(self, file_type):
        file_path = filedialog.askopenfilename(
            filetypes=self.get_file_types(file_type))
        if not file_path:
            return
        
        try:
            if file_type == 'csv':
                self.data = pd.read_csv(file_path)
            elif file_type == 'excel':
                self.data = pd.read_excel(file_path)
            elif file_type == 'json':
                self.data = pd.read_json(file_path)
            
            self.display_data()
            self.app.enable_controls()
            self.app.update_column_comboboxes()
            self.info_label.config(text=f"Data loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            self.export_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def get_file_types(self, file_type):
        if file_type == 'csv':
            return [("CSV files", "*.csv"), ("All files", "*.*")]
        elif file_type == 'excel':
            return [("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        elif file_type == 'json':
            return [("JSON files", "*.json"), ("All files", "*.*")]
    
    def display_data(self):
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        if self.data is not None:
            self.data_text.insert(tk.END, self.data.head(100).to_string())
        self.data_text.config(state=tk.DISABLED)
    
    def export_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("JSON files", "*.json")]
        )
        if not file_path:
            return
        
        try:
            if file_path.endswith('.csv'):
                self.data.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx'):
                self.data.to_excel(file_path, index=False)
            elif file_path.endswith('.json'):
                self.data.to_json(file_path)
            
            messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")