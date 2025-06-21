import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import json
import os
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['font.size'] = 10

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Data Analysis Tool")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Start maximized
        self.data = None
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.export_dir = os.path.expanduser("~")
        self.plot_config = {
            'color': '#3498db',
            'title': 'Data Visualization',
            'xlabel': 'X Axis',
            'ylabel': 'Y Axis',
            'style': 'classic',
            'palette': 'viridis'
        }
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.data_tab = ttk.Frame(self.notebook)
        self.preprocess_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.data_tab, text="Data")
        self.notebook.add(self.preprocess_tab, text="Preprocessing")
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.notebook.add(self.analysis_tab, text="Analysis")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f5f5f5')
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', background='#f5f5f5')
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        
        # Initialize tabs
        self.setup_data_tab()
        self.setup_preprocess_tab()
        self.setup_visualization_tab()
        self.setup_analysis_tab()
    
    def setup_data_tab(self):
        # Header
        header_frame = ttk.Frame(self.data_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="Data Loading & Exploration", style='Header.TLabel').pack()
        
        # File Loading
        file_frame = ttk.LabelFrame(self.data_tab, text="Data Import")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Load CSV", command=lambda: self.load_data('csv')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Load Excel", command=lambda: self.load_data('excel')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Load JSON", command=lambda: self.load_data('json')).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Data Display
        display_frame = ttk.Frame(self.data_tab)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.data_text = scrolledtext.ScrolledText(
            display_frame, wrap=tk.NONE, width=120, height=25
        )
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Data Info
        info_frame = ttk.Frame(self.data_tab)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="No data loaded")
        self.info_label.pack(side=tk.LEFT)
        
        ttk.Button(info_frame, text="Export Data", command=self.export_data, state='disabled').pack(side=tk.RIGHT)
    
    def setup_preprocess_tab(self):
        # Header
        header_frame = ttk.Frame(self.preprocess_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="Data Preprocessing", style='Header.TLabel').pack()
        
        # Preprocessing options
        options_frame = ttk.LabelFrame(self.preprocess_tab, text="Preprocessing Options")
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
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter, state='disabled').grid(row=0, column=6, padx=5)
        
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
        
        ttk.Button(type_frame, text="Convert", command=self.convert_type, state='disabled').grid(row=0, column=4, padx=5)
        
        # Apply preprocessing
        apply_frame = ttk.Frame(self.preprocess_tab)
        apply_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(apply_frame, text="Apply Preprocessing", command=self.apply_preprocessing, state='disabled').pack()
    
    def setup_visualization_tab(self):
        # Header
        header_frame = ttk.Frame(self.visualization_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="Data Visualization", style='Header.TLabel').pack()
        
        # Controls
        control_frame = ttk.Frame(self.visualization_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Column selection
        col_frame = ttk.LabelFrame(control_frame, text="Columns")
        col_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        ttk.Label(col_frame, text="X Column:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.x_col = ttk.Combobox(col_frame, state='disabled', width=20)
        self.x_col.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(col_frame, text="Y Column:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.y_col = ttk.Combobox(col_frame, state='disabled', width=20)
        self.y_col.grid(row=0, column=3, padx=5, pady=5)
        
        # Plot selection
        plot_frame = ttk.LabelFrame(control_frame, text="Plot Type")
        plot_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        self.plot_type = ttk.Combobox(plot_frame, values=[
            "Histogram", "Box Plot", "Scatter Plot", "Line Chart", 
            "Bar Chart", "Heatmap", "Pair Plot", "Regression Plot",
            "Time Series Decomposition"
        ], state='disabled', width=20)
        self.plot_type.grid(row=0, column=0, padx=5, pady=5)
        self.plot_type.bind('<<ComboboxSelected>>', self.on_plot_type_change)
        
        # Styling options
        style_frame = ttk.LabelFrame(control_frame, text="Style")
        style_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        ttk.Label(style_frame, text="Color:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.color_var = tk.StringVar(value="#3498db")
        ttk.Entry(style_frame, textvariable=self.color_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(style_frame, text="Palette:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.palette_var = ttk.Combobox(style_frame, values=[
            'viridis', 'plasma', 'inferno', 'magma', 'cividis',
            'coolwarm', 'rainbow', 'tab10', 'Set2'
        ], width=10)
        self.palette_var.set('viridis')
        self.palette_var.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(style_frame, text="Style:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.style_var = ttk.Combobox(style_frame, values=[
            'ggplot', 'classic', 'dark_background', 'bmh'
        ], width=10)
        self.style_var.set('seaborn')
        self.style_var.grid(row=0, column=3, padx=5, pady=2)
        
        # Titles
        title_frame = ttk.LabelFrame(control_frame, text="Titles")
        title_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        ttk.Label(title_frame, text="Title:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.title_var = tk.StringVar(value="Data Visualization")
        ttk.Entry(title_frame, textvariable=self.title_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(title_frame, text="X Label:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.xlabel_var = tk.StringVar(value="X Axis")
        ttk.Entry(title_frame, textvariable=self.xlabel_var, width=15).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(title_frame, text="Y Label:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.ylabel_var = tk.StringVar(value="Y Axis")
        ttk.Entry(title_frame, textvariable=self.ylabel_var, width=15).grid(row=0, column=3, padx=5, pady=2)
        
        # Action buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Generate Plot", command=self.generate_plot, state='disabled').grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Export Plot", command=self.export_plot, state='disabled').grid(row=1, column=0, padx=5, pady=5)
        
        # Plot area
        plot_area = ttk.Frame(self.visualization_tab)
        plot_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.plot_container = ttk.Frame(plot_area)
        self.plot_container.pack(fill=tk.BOTH, expand=True)
    
    def setup_analysis_tab(self):
        # Header
        header_frame = ttk.Frame(self.analysis_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="Data Analysis", style='Header.TLabel').pack()
        
        # Controls
        control_frame = ttk.Frame(self.analysis_tab)
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
        ttk.Button(control_frame, text="Run Analysis", command=self.run_analysis, state='disabled').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Results", command=self.export_analysis, state='disabled').pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.Frame(self.analysis_tab)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, wrap=tk.WORD, width=120, height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
    
    def load_data(self, file_type):
        file_path = filedialog.askopenfilename()
        filetypes=self.get_file_types(file_type)
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
            self.enable_controls()
            self.update_column_comboboxes()
            self.info_label.config(text=f"Data loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            
            # Enable export button
            self.data_tab.winfo_children()[3].winfo_children()[1].config(state=tk.NORMAL)
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
    
    def enable_controls(self):
        # Enable controls in all tabs
        self.preprocess_tab.winfo_children()[2].winfo_children()[-1].config(state=tk.NORMAL)  # Apply preprocessing button
        self.filter_col.config(state='readonly')
        self.filter_cond.config(state='readonly')
        self.filter_val.config(state='normal')
        self.type_col.config(state='readonly')
        self.type_target.config(state='readonly')
        self.filter_frame = self.preprocess_tab.winfo_children()[1].winfo_children()[1]
        self.filter_frame.winfo_children()[-1].config(state=tk.NORMAL)  # Apply filter button
        self.type_frame = self.preprocess_tab.winfo_children()[1].winfo_children()[2]
        self.type_frame.winfo_children()[-1].config(state=tk.NORMAL)  # Convert button
        
        # Visualization tab
        self.x_col.config(state='readonly')
        self.y_col.config(state='readonly')
        self.plot_type.config(state='readonly')
        self.visualization_tab.winfo_children()[1].winfo_children()[-1].winfo_children()[0].config(state=tk.NORMAL)  # Generate plot
        self.visualization_tab.winfo_children()[1].winfo_children()[-1].winfo_children()[1].config(state=tk.NORMAL)  # Export plot
        
        # Analysis tab
        self.analysis_type.config(state='readonly')
        self.analysis_tab.winfo_children()[1].winfo_children()[-2].config(state=tk.NORMAL)  # Run analysis
        self.analysis_tab.winfo_children()[1].winfo_children()[-1].config(state=tk.NORMAL)  # Export results
    
    def update_column_comboboxes(self):
        if self.data is not None:
            columns = list(self.data.columns)
            self.filter_col['values'] = columns
            self.type_col['values'] = columns
            self.x_col['values'] = columns
            self.y_col['values'] = columns
            self.var1['values'] = columns
            self.var2['values'] = columns
            
            if columns:
                self.filter_col.set(columns[0])
                self.type_col.set(columns[0])
                self.x_col.set(columns[0])
                if len(columns) > 1:
                    self.y_col.set(columns[1])
                    self.var1.set(columns[0])
                    self.var2.set(columns[1])
                else:
                    self.y_col.set(columns[0])
                    self.var1.set(columns[0])
                    self.var2.set(columns[0])
    
    def on_plot_type_change(self, event=None):
        plot_type = self.plot_type.get()
        # Disable Y column for plots that don't need it
        if plot_type in ["Histogram", "Box Plot", "Bar Chart", "Heatmap", "Pair Plot", "Time Series Decomposition"]:
            self.y_col.config(state='disabled')
        else:
            self.y_col.config(state='readonly')
    
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
    
    def apply_filter(self):
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
            self.data = self.data.query(expr)
            self.display_data()
            self.info_label.config(text=f"Filter applied: {self.data.shape[0]} rows remaining")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid filter expression:\n{str(e)}")
    
    def convert_type(self):
        col = self.type_col.get()
        target_type = self.type_target.get()
        
        if not col or not target_type:
            return
        
        try:
            if target_type == "numeric":
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            elif target_type == "string":
                self.data[col] = self.data[col].astype(str)
            elif target_type == "datetime":
                self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
            elif target_type == "category":
                self.data[col] = self.data[col].astype('category')
            
            self.display_data()
            messagebox.showinfo("Success", f"Column '{col}' converted to {target_type}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
    
    def apply_preprocessing(self):
        if self.data is None:
            return
        
        # Handle missing values
        method = self.missing_var.get()
        if method == "drop":
            self.data = self.data.dropna()
        elif method == "mean":
            self.data = self.data.fillna(self.data.mean(numeric_only=True))
        elif method == "median":
            self.data = self.data.fillna(self.data.median(numeric_only=True))
        elif method == "mode":
            self.data = self.data.fillna(self.data.mode().iloc[0])
        elif method == "custom":
            try:
                val = float(self.custom_val.get()) if self.custom_val.get() else 0
                self.data = self.data.fillna(val)
            except ValueError:
                messagebox.showerror("Error", "Invalid custom value for missing data")
                return
        
        self.display_data()
        self.info_label.config(text=f"Preprocessing applied: {self.data.shape[0]} rows")
    
    def generate_plot(self):
        if self.data is None:
            return
        
        # Clear previous plot
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.toolbar:
            self.toolbar.destroy()
        
        # Get plot parameters
        x_col = self.x_col.get()
        y_col = self.y_col.get() if self.y_col['state'] == 'readonly' else None
        plot_type = self.plot_type.get()
        
        # Apply style
        plt.style.use(self.style_var.get())
        
        # Create figure
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        # Get color
        color = self.color_var.get()
        palette = self.palette_var.get()
        
        try:
            if plot_type == "Histogram":
                self.data[x_col].hist(ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Box Plot":
                sns.boxplot(y=self.data[x_col], ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Scatter Plot":
                self.data.plot.scatter(x=x_col, y=y_col, ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Line Chart":
                self.data.plot(x=x_col, y=y_col, ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Bar Chart":
                if pd.api.types.is_numeric_dtype(self.data[x_col]):
                    self.data[x_col].value_counts().head(10).plot(ax=ax, kind='bar', color=color)
                else:
                    self.data[x_col].value_counts().head(10).plot(ax=ax, kind='bar', color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Heatmap":
                num_cols = self.data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    messagebox.showwarning("Warning", "Heatmap requires at least two numeric columns")
                    return
                corr = self.data[num_cols].corr()
                sns.heatmap(corr, annot=True, fmt=".2f", ax=ax, cmap=palette)
                ax.set_title(self.title_var.get())
            
            elif plot_type == "Pair Plot":
                num_cols = self.data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    messagebox.showwarning("Warning", "Pair plot requires at least two numeric columns")
                    return
                
                pair_fig = sns.pairplot(self.data[num_cols], palette=palette)
                pair_fig.fig.suptitle(self.title_var.get(), y=1.02)
                
                # Embed in Tkinter
                self.canvas = FigureCanvasTkAgg(pair_fig.fig, self.plot_container)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Add toolbar
                self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
                self.toolbar.update()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                return
            
            elif plot_type == "Regression Plot":
                if not pd.api.types.is_numeric_dtype(self.data[x_col]) or not pd.api.types.is_numeric_dtype(self.data[y_col]):
                    messagebox.showwarning("Warning", "Regression plot requires two numeric columns")
                    return
                
                sns.regplot(x=x_col, y=y_col, data=self.data, ax=ax, color=color, 
                            line_kws={'color': 'red'}, scatter_kws={'alpha': 0.5})
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
                
                # Add regression equation
                X = self.data[x_col].values.reshape(-1, 1)
                y = self.data[y_col].values
                model = LinearRegression().fit(X, y)
                r_sq = model.score(X, y)
                equation = f"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}\nR² = {r_sq:.4f}"
                ax.text(0.05, 0.95, equation, transform=ax.transAxes, 
                       fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            elif plot_type == "Time Series Decomposition":
                if not pd.api.types.is_datetime64_any_dtype(self.data[x_col]):
                    messagebox.showwarning("Warning", "Time series requires datetime column for X")
                    return
                
                if not y_col:
                    messagebox.showwarning("Warning", "Please select a Y column")
                    return
                
                # Set datetime index
                ts_data = self.data.set_index(x_col)[y_col]
                ts_data = ts_data.asfreq('D').fillna(method='ffill')  # Handle missing dates
                
                # Decompose
                decomposition = seasonal_decompose(ts_data, model='additive', period=30)
                
                # Create a 2x2 grid of plots
                self.figure, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
                self.figure.suptitle(f"Time Series Decomposition: {y_col}", fontsize=16)
                
                # Original time series
                ts_data.plot(ax=ax1, color=color)
                ax1.set_title('Original Time Series')
                ax1.set_ylabel(y_col)
                
                # Trend component
                decomposition.trend.plot(ax=ax2, color='green')
                ax2.set_title('Trend Component')
                
                # Seasonal component
                decomposition.seasonal.plot(ax=ax3, color='purple')
                ax3.set_title('Seasonal Component')
                
                # Residual component
                decomposition.resid.plot(ax=ax4, color='red')
                ax4.set_title('Residual Component')
                
                plt.tight_layout()
                plt.subplots_adjust(top=0.9)
            
            # Embed in Tkinter
            self.canvas = FigureCanvasTkAgg(self.figure, self.plot_container)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Enable export button
            self.visualization_tab.winfo_children()[1].winfo_children()[-1].winfo_children()[1].config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Failed to generate plot:\n{str(e)}")
    
    def run_analysis(self):
        if self.data is None:
            return
        
        analysis_type = self.analysis_type.get()
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        try:
            if analysis_type == "Descriptive Statistics":
                stats = self.data.describe(include='all').to_string()
                self.results_text.insert(tk.END, "Descriptive Statistics:\n\n")
                self.results_text.insert(tk.END, stats)
            
            elif analysis_type == "Correlation Matrix":
                num_cols = self.data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    self.results_text.insert(tk.END, "Not enough numeric columns for correlation matrix")
                    return
                
                corr = self.data[num_cols].corr()
                self.results_text.insert(tk.END, "Correlation Matrix:\n\n")
                self.results_text.insert(tk.END, corr.to_string())
            
            elif analysis_type == "Regression Analysis":
                x_col = self.var1.get()
                y_col = self.var2.get()
                
                if not pd.api.types.is_numeric_dtype(self.data[x_col]) or not pd.api.types.is_numeric_dtype(self.data[y_col]):
                    self.results_text.insert(tk.END, "Both variables must be numeric for regression analysis")
                    return
                
                X = self.data[x_col].values.reshape(-1, 1)
                y = self.data[y_col].values
                
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
            self.analysis_tab.winfo_children()[1].winfo_children()[-1].config(state=tk.NORMAL)
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Analysis failed:\n{str(e)}")
        
        self.results_text.config(state=tk.DISABLED)
    
    def export_data(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.export_dir,
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
    
    def export_plot(self):
        if not self.figure:
            messagebox.showwarning("Warning", "No plot to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            initialdir=self.export_dir,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        if not file_path:
            return
        
        try:
            self.figure.savefig(file_path, bbox_inches='tight')
            messagebox.showinfo("Success", f"Plot exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export plot:\n{str(e)}")
    
    def export_analysis(self):
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No analysis results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            initialdir=self.export_dir,
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

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()