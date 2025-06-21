import tkinter as tk
from tkinter import ttk, scrolledtext
from tabs.data import DataManager
from tabs.preprocessing import PreprocessingManager
from tabs.visualization import VisualizationManager
from tabs.analysis import AnalysisManager

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Data Analysis Tool")
        # self.root.geometry("1400x900")
        self.root.state('zoomed')
        self.data = None
        self.figure = None
        self.canvas = None
        self.toolbar = None
        
        # Set bold font for notebook tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'))
        
        # Initialize managers
        self.data_manager = DataManager(self)
        self.preprocess_manager = PreprocessingManager(self)
        self.visualization_manager = VisualizationManager(self)
        self.analysis_manager = AnalysisManager(self)
        
        # Create main notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.data_tab = self.create_data_tab()
        self.preprocess_tab = self.create_preprocess_tab()
        self.visualization_tab = self.create_visualization_tab()
        self.analysis_tab = self.create_analysis_tab()
        
        # Add tabs to notebook
        self.notebook.add(self.data_tab, text="Data")
        self.notebook.add(self.preprocess_tab, text="Preprocessing")
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.notebook.add(self.analysis_tab, text="Analysis")
    
    def create_data_tab(self):
        tab = ttk.Frame(self.notebook)
        self.data_manager.setup_ui(tab)
        return tab
    
    def create_preprocess_tab(self):
        tab = ttk.Frame(self.notebook)
        self.preprocess_manager.setup_ui(tab)
        return tab
    
    def create_visualization_tab(self):
        tab = ttk.Frame(self.notebook)
        self.visualization_manager.setup_ui(tab)
        return tab
    
    def create_analysis_tab(self):
        tab = ttk.Frame(self.notebook)
        self.analysis_manager.setup_ui(tab)
        return tab
    
    def get_data(self):
        return self.data_manager.data
    
    def update_data_display(self):
        self.data_manager.display_data()
    
    def update_column_comboboxes(self):
        self.preprocess_manager.update_column_comboboxes()
        self.visualization_manager.update_column_comboboxes()
        self.analysis_manager.update_column_comboboxes()
    
    def enable_controls(self):
        self.preprocess_manager.enable_controls()
        self.visualization_manager.enable_controls()
        self.analysis_manager.enable_controls()