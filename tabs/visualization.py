import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose

class VisualizationManager:
    def __init__(self, app):
        self.app = app
        self.figure = None
        self.canvas = None
        self.toolbar = None
    
    def setup_ui(self, parent):
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        ttk.Label(header_frame, text="Data Visualization", style='Header.TLabel').pack()
        
        # Controls
        control_frame = ttk.Frame(parent)
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
        self.style_var.set('classic')
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
        
        self.plot_btn = ttk.Button(btn_frame, text="Generate Plot", command=self.generate_plot, state='disabled')
        self.plot_btn.grid(row=0, column=0, padx=5)
        self.export_btn = ttk.Button(btn_frame, text="Export Plot", command=self.export_plot, state='disabled')
        self.export_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Plot area
        plot_area = ttk.Frame(parent)
        plot_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.plot_container = ttk.Frame(plot_area)
        self.plot_container.pack(fill=tk.BOTH, expand=True)
    
    def enable_controls(self):
        self.x_col.config(state='readonly')
        self.y_col.config(state='readonly')
        self.plot_type.config(state='readonly')
        self.plot_btn.config(state=tk.NORMAL)
    
    def update_column_comboboxes(self):
        data = self.app.get_data()
        if data is not None:
            columns = list(data.columns)
            self.x_col['values'] = columns
            self.y_col['values'] = columns
            
            if columns:
                self.x_col.set(columns[0])
                if len(columns) > 1:
                    self.y_col.set(columns[1])
                else:
                    self.y_col.set(columns[0])
    
    def on_plot_type_change(self, event=None):
        plot_type = self.plot_type.get()
        # Disable Y column for plots that don't need it
        if plot_type in ["Histogram", "Box Plot", "Bar Chart", "Heatmap", "Pair Plot", "Time Series Decomposition"]:
            self.y_col.config(state='disabled')
        else:
            self.y_col.config(state='readonly')
    
    def generate_plot(self):
        data = self.app.get_data()
        if data is None:
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
                data[x_col].hist(ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Box Plot":
                sns.boxplot(y=data[x_col], ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Scatter Plot":
                data.plot.scatter(x=x_col, y=y_col, ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Line Chart":
                data.plot(x=x_col, y=y_col, ax=ax, color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Bar Chart":
                if pd.api.types.is_numeric_dtype(data[x_col]):
                    data[x_col].value_counts().head(10).plot(ax=ax, kind='bar', color=color)
                else:
                    data[x_col].value_counts().head(10).plot(ax=ax, kind='bar', color=color)
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
            
            elif plot_type == "Heatmap":
                num_cols = data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    messagebox.showwarning("Warning", "Heatmap requires at least two numeric columns")
                    return
                corr = data[num_cols].corr()
                sns.heatmap(corr, annot=True, fmt=".2f", ax=ax, cmap=palette)
                ax.set_title(self.title_var.get())
            
            elif plot_type == "Pair Plot":
                num_cols = data.select_dtypes(include=np.number).columns.tolist()
                if len(num_cols) < 2:
                    messagebox.showwarning("Warning", "Pair plot requires at least two numeric columns")
                    return
                
                pair_fig = sns.pairplot(data[num_cols], palette=palette)
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
                if not pd.api.types.is_numeric_dtype(data[x_col]) or not pd.api.types.is_numeric_dtype(data[y_col]):
                    messagebox.showwarning("Warning", "Regression plot requires two numeric columns")
                    return
                
                sns.regplot(x=x_col, y=y_col, data=data, ax=ax, color=color, 
                            line_kws={'color': 'red'}, scatter_kws={'alpha': 0.5})
                ax.set_title(self.title_var.get())
                ax.set_xlabel(self.xlabel_var.get())
                ax.set_ylabel(self.ylabel_var.get())
                
                # Add regression equation
                X = data[x_col].values.reshape(-1, 1)
                y = data[y_col].values
                model = LinearRegression().fit(X, y)
                r_sq = model.score(X, y)
                equation = f"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}\nR² = {r_sq:.4f}"
                ax.text(0.05, 0.95, equation, transform=ax.transAxes, 
                       fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            elif plot_type == "Time Series Decomposition":
                if not pd.api.types.is_datetime64_any_dtype(data[x_col]):
                    messagebox.showwarning("Warning", "Time series requires datetime column for X")
                    return
                
                if not y_col:
                    messagebox.showwarning("Warning", "Please select a Y column")
                    return
                
                # Set datetime index
                ts_data = data.set_index(x_col)[y_col]
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
            self.export_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Failed to generate plot:\n{str(e)}")
    
    def export_plot(self):
        if not self.figure:
            messagebox.showwarning("Warning", "No plot to export")
            return
        
        file_path = filedialog.asksaveasfilename(
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