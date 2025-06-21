import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

class PreprocessingManager:
    def __init__(self, app):
        self.app = app
    
    def setup_ui(self, parent):
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        ttk.Label(header_frame, text="Data Preprocessing", style='Header.TLabel').pack()
        
        # Preprocessing options
        options_frame = ttk.LabelFrame(parent, text="Preprocessing Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Handling missing values
        missing_frame = ttk.LabelFrame(options_frame, text="Missing Values")
        missing_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.missing_var = tk.StringVar(value="drop")
        ttk.Radiobutton(missing_frame, text="Drop rows with missing values", 
                        variable=self.missing_var, value="drop").pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with mean", 
                        variable=self.missing_var, value="mean").pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with median", 
                        variable=self.missing_var, value="median").pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with mode", 
                        variable=self.missing_var, value="mode").pack(anchor=tk.W)
        ttk.Radiobutton(missing_frame, text="Fill with specific value:", 
                        variable=self.missing_var, value="custom").pack(side=tk.LEFT, anchor=tk.W)
        self.custom_val = ttk.Entry(missing_frame, width=10)
        self.custom_val.pack(side=tk.LEFT, padx=5)
        
        # Data filtering
        filter_frame = ttk.LabelFrame(options_frame, text="Data Filtering")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Column:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filter_col = ttk.Combobox(filter_frame, state='disabled', width=20)
        self.filter_col.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Condition:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.filter_cond = ttk.Combobox(filter_frame, values=[">", ">=", "<", "<=", "==", "!="], 
                                      state='disabled', width=5)
        self.filter_cond.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Value:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.filter_val = ttk.Entry(filter_frame, state='disabled', width=10)
        self.filter_val.grid(row=0, column=5, padx=5, pady=5)
        
        self.apply_filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter, state='disabled')
        self.apply_filter_btn.grid(row=0, column=6, padx=5)
        
        # Data type conversion
        type_frame = ttk.LabelFrame(options_frame, text="Data Type Conversion")
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Column:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_col = ttk.Combobox(type_frame, state='disabled', width=20)
        self.type_col.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Convert to:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.type_target = ttk.Combobox(type_frame, values=["numeric", "string", "datetime", "category"], 
                                      state='disabled', width=10)
        self.type_target.grid(row=0, column=3, padx=5, pady=5)
        
        self.convert_btn = ttk.Button(type_frame, text="Convert", command=self.convert_type, state='disabled')
        self.convert_btn.grid(row=0, column=4, padx=5)
        
        # Apply preprocessing
        apply_frame = ttk.Frame(parent)
        apply_frame.pack(fill=tk.X, padx=10, pady=10)
        self.apply_preprocess_btn = ttk.Button(apply_frame, text="Apply Preprocessing", command=self.apply_preprocessing, state='disabled')
        self.apply_preprocess_btn.pack()
    
    def enable_controls(self):
        self.apply_preprocess_btn.config(state=tk.NORMAL)
        self.filter_col.config(state='readonly')
        self.filter_cond.config(state='readonly')
        self.filter_val.config(state='normal')
        self.type_col.config(state='readonly')
        self.type_target.config(state='readonly')
        self.apply_filter_btn.config(state=tk.NORMAL)
        self.convert_btn.config(state=tk.NORMAL)
    
    def update_column_comboboxes(self):
        data = self.app.get_data()
        if data is not None:
            columns = list(data.columns)
            self.filter_col['values'] = columns
            self.type_col['values'] = columns
            
            if columns:
                self.filter_col.set(columns[0])
                self.type_col.set(columns[0])
    
    def apply_filter(self):
        data = self.app.get_data()
        col = self.filter_col.get()
        cond = self.filter_cond.get()
        val = self.filter_val.get()
        
        if not col or not cond or not val:
            messagebox.showwarning("Warning", "Please fill all filter fields")
            return
        
        try:
            # Try to convert value to number
            try:
                val = float(val)
            except ValueError:
                pass  # Keep as string if conversion fails
                
            # Create filter expression
            expr = f"`{col}` {cond} {repr(val)}"
            self.app.data_manager.data = data.query(expr)
            self.app.update_data_display()
            self.app.data_manager.info_label.config(text=f"Filter applied: {self.app.get_data().shape[0]} rows remaining")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid filter expression:\n{str(e)}")
    
    def convert_type(self):
        data = self.app.get_data()
        col = self.type_col.get()
        target_type = self.type_target.get()
        
        if not col or not target_type:
            return
        
        try:
            if target_type == "numeric":
                data[col] = pd.to_numeric(data[col], errors='coerce')
            elif target_type == "string":
                data[col] = data[col].astype(str)
            elif target_type == "datetime":
                data[col] = pd.to_datetime(data[col], errors='coerce')
            elif target_type == "category":
                data[col] = data[col].astype('category')
            
            self.app.update_data_display()
            messagebox.showinfo("Success", f"Column '{col}' converted to {target_type}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
    
    def apply_preprocessing(self):
        data = self.app.get_data()
        if data is None:
            return
        
        # Handle missing values
        method = self.missing_var.get()
        if method == "drop":
            self.app.data_manager.data = data.dropna()
        elif method == "mean":
            self.app.data_manager.data = data.fillna(data.mean(numeric_only=True))
        elif method == "median":
            self.app.data_manager.data = data.fillna(data.median(numeric_only=True))
        elif method == "mode":
            self.app.data_manager.data = data.fillna(data.mode().iloc[0])
        elif method == "custom":
            try:
                val = float(self.custom_val.get()) if self.custom_val.get() else 0
                self.app.data_manager.data = data.fillna(val)
            except ValueError:
                messagebox.showerror("Error", "Invalid custom value for missing data")
                return
        
        self.app.update_data_display()
        self.app.data_manager.info_label.config(text=f"Preprocessing applied: {self.app.get_data().shape[0]} rows")