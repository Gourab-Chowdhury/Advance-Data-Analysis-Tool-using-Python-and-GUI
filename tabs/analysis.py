import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from sklearn.linear_model import LinearRegression

class AnalysisManager:
    def __init__(self, app):
        self.app = app
    
    def setup_ui(self, parent):
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        ttk.Label(header_frame, text="Data Analysis", style='Header.TLabel').pack()
        
        # Controls
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Analysis Type:").pack(side=tk.LEFT, padx=5)
        self.analysis_type = ttk.Combobox(control_frame, values=[
            "Descriptive Statistics", "Correlation Matrix", "Regression Analysis"
        ], state='disabled', width=25)
        self.analysis_type.pack(side=tk.LEFT, padx=5)
        self.analysis_type.bind('<<ComboboxSelected>>', self.on_analysis_type_change)
        
        # Variable selection
        var_frame = ttk.Frame(control_frame)
        var_frame.pack(side=tk.LEFT, padx=10)
        
        self.var1_label = ttk.Label(var_frame, text="Independent Variable:")
        self.var1_label.pack(side=tk.LEFT, padx=5)
        self.var1 = ttk.Combobox(var_frame, state='disabled', width=15)
        self.var1.pack(side=tk.LEFT, padx=5)
        
        self.var2_label = ttk.Label(var_frame, text="Dependent Variable:")
        self.var2_label.pack(side=tk.LEFT, padx=5)
        self.var2 = ttk.Combobox(var_frame, state='disabled', width=15)
        self.var2.pack(side=tk.LEFT, padx=5)
        
        # Run analysis button
        self.run_btn = ttk.Button(control_frame, text="Run Analysis", command=self.run_analysis, state='disabled')
        self.run_btn.pack(side=tk.LEFT, padx=5)
        self.export_btn = ttk.Button(control_frame, text="Export Results", command=self.export_analysis, state='disabled')
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, wrap=tk.WORD, width=120, height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
    
    def enable_controls(self):
        self.analysis_type.config(state='readonly')
        self.run_btn.config(state=tk.NORMAL)
    
    def update_column_comboboxes(self):
        data = self.app.get_data()
        if data is not None:
            columns = list(data.columns)
            self.var1['values'] = columns
            self.var2['values'] = columns
            
            if columns:
                self.var1.set(columns[0])
                if len(columns) > 1:
                    self.var2.set(columns[1])
                else:
                    self.var2.set(columns[0])
    
    def on_analysis_type_change(self, event=None):
        analysis_type = self.analysis_type.get()
        if analysis_type == "Regression Analysis":
            self.var1_label.config(text="Independent Variable:")
            self.var2_label.config(text="Dependent Variable:")
            self.var1.config(state='readonly')
            self.var2.config(state='readonly')
        else:
            self.var1.config(state='disabled')
            self.var2.config(state='disabled')
    
    def run_analysis(self):
        data = self.app.get_data()
        if data is None:
            return
        
        analysis_type = self.analysis_type.get()
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        try:
            if analysis_type == "Descriptive Statistics":
                stats = data.describe(include='all').to_string()
                self.results_text.insert(tk.END, "Descriptive Statistics:\n\n")
                self.results_text.insert(tk.END, stats)
            
            elif analysis_type == "Correlation Matrix":
                num_cols = data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    self.results_text.insert(tk.END, "Not enough numeric columns for correlation matrix")
                    return
                
                corr = data[num_cols].corr()
                self.results_text.insert(tk.END, "Correlation Matrix:\n\n")
                self.results_text.insert(tk.END, corr.to_string())
            
            elif analysis_type == "Regression Analysis":
                x_col = self.var1.get()
                y_col = self.var2.get()
                
                if not pd.api.types.is_numeric_dtype(data[x_col]) or not pd.api.types.is_numeric_dtype(data[y_col]):
                    self.results_text.insert(tk.END, "Both variables must be numeric for regression analysis")
                    return
                
                X = data[x_col].values.reshape(-1, 1)
                y = data[y_col].values
                
                model = LinearRegression().fit(X, y)
                r_sq = model.score(X, y)
                intercept = model.intercept_
                slope = model.coef_[0]
                
                self.results_text.insert(tk.END, f"Regression Analysis: {y_col} ~ {x_col}\n\n")
                self.results_text.insert(tk.END, f"Regression Equation: y = {slope:.4f}x + {intercept:.4f}\n")
                self.results_text.insert(tk.END, f"Coefficient of Determination (R²): {r_sq:.4f}\n\n")
                self.results_text.insert(tk.END, "Interpretation:\n")
                self.results_text.insert(tk.END, f"- For each unit increase in {x_col}, {y_col} changes by {slope:.4f}\n")
                self.results_text.insert(tk.END, f"- When {x_col} is 0, {y_col} is {intercept:.4f}\n")
                self.results_text.insert(tk.END, f"- The model explains {r_sq*100:.2f}% of the variability in {y_col}")
            
            # Enable export button
            self.export_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Analysis failed:\n{str(e)}")
        
        self.results_text.config(state=tk.DISABLED)
    
    def export_analysis(self):
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No analysis results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as f:
                f.write(self.results_text.get(1.0, tk.END))
            messagebox.showinfo("Success", f"Results exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results:\n{str(e)}")