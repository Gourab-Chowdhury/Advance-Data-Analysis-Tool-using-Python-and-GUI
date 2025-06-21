# Advanced Data Analysis Tool using Python and GUI

![Advanced Data Analysis Tool Screenshot](screenshot\Data Analysis.png)

The Advanced Data Analysis Tool is a comprehensive Python application designed for performing statistical analysis, data preprocessing, and visualization on various data formats. With its intuitive graphical interface, users can easily explore, clean, analyze, and visualize datasets without writing any code.

## Key Features

### 📊 Data Management
- Import data from multiple formats: CSV, Excel, JSON
- Preview datasets with first 100 rows display
- Export processed data to CSV, Excel, or JSON
- View dataset dimensions and basic information

### 🧹 Data Preprocessing
- Handle missing values (drop rows, fill with mean/median/mode/custom)
- Filter data based on column conditions
- Convert data types (numeric, string, datetime, category)
- Apply multiple preprocessing steps sequentially

### 📈 Visualization
- Create various plot types:
  - Histograms
  - Box plots
  - Scatter plots
  - Line charts
  - Bar charts
  - Heatmaps
  - Pair plots
  - Regression plots
  - Time series decomposition
- Customize plot appearance:
  - Color schemes and palettes
  - Plot styles (seaborn, ggplot, dark theme, etc.)
  - Titles and axis labels
- Interactive plot navigation (zoom, pan, save)
- Export plots to PNG, JPEG, PDF, or SVG

### 📊 Statistical Analysis
- Generate descriptive statistics
- Calculate correlation matrices
- Perform linear regression analysis
- Display regression equations and R-squared values
- Interpret regression results
- Export analysis reports

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/advanced-data-analysis-tool.git
   cd advanced-data-analysis-tool
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

The application requires the following Python packages:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- statsmodels
- openpyxl (for Excel support)

All dependencies are listed in the `requirements.txt` file.

## Usage

1. **Launch the application**:
   ```bash
   python main.py
   ```

2. **Load your data**:
   - Go to the "Data" tab
   - Click "Load CSV", "Load Excel", or "Load JSON"
   - Select your data file

3. **Preprocess your data** (optional):
   - Go to the "Preprocessing" tab
   - Handle missing values
   - Apply filters
   - Convert data types
   - Click "Apply Preprocessing"

4. **Visualize your data**:
   - Go to the "Visualization" tab
   - Select X and Y columns
   - Choose a plot type
   - Customize appearance
   - Click "Generate Plot"

5. **Analyze your data**:
   - Go to the "Analysis" tab
   - Select an analysis type
   - Choose variables for regression (if applicable)
   - Click "Run Analysis"

6. **Export results**:
   - Export processed data from the Data tab
   - Export plots from the Visualization tab
   - Export analysis results from the Analysis tab

## Project Structure

```
advanced-data-analysis-tool/
tabs/
 ├── data.py             # Data loading and management
 ├── preprocessing.py    # Data preprocessing functions
 ├── visualization.py    # Data visualization functions
 ├── analysis.py         # Statistical analysis functions
├── main.py              # Application entry point
├── gui.py               # Main GUI implementation 
├── requirements.txt     # Dependencies list
└── README.md            # Project documentation
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or feature requests, please open an issue on the GitHub repository.
