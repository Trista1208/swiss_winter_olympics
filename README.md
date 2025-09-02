# 🏔️ Swiss Olympic Biathlon Analysis Dashboard

A comprehensive analysis system for Swiss biathlon athletes' Olympic qualification for the 2026 Milano Cortina Olympics.

## 🚀 Quick Start

### Option 1: Web Dashboard (Recommended)
```bash
python run_dashboard.py
```
Then open your browser to `http://localhost:8501`

### Option 2: Command Line Analysis
```bash
python run_analysis.py
```

### Option 3: Individual Scripts
```bash
python biathlon_analysis.py      # Basic data analysis
python qualification_checker.py  # Qualification checking
```

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Trista1208/swiss_winter_olympics.git
cd swiss_winter_olympics
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
python run_dashboard.py
```

## 📊 Features

### 🌐 Web Dashboard
- **Interactive Overview**: Team qualification status and statistics
- **Athlete Profiles**: Detailed information for each athlete
- **Performance Analysis**: Charts and trends for individual athletes
- **Qualification Details**: Route-by-route breakdown and criteria

### 📈 Analysis Components
- **Data Processing**: Cleans and analyzes biathlon results
- **Qualification System**: Implements all 5 Olympic qualification routes
- **Performance Metrics**: Rankings, trends, and statistics
- **Reporting**: Comprehensive athlete and team reports

## 🎯 Qualification Routes

The system evaluates athletes against 5 qualification routes defined by Swiss Olympic:

1. **Route 1**: Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26
2. **Route 2**: 1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26  
3. **Route 3**: 1x Top-15 in World Cup 2025/26
4. **Route 4**: 2x Top-25 in World Cup 2025/26
5. **Route 5**: 1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26

## 📁 Project Structure

```
swiss_winter_olympics/
├── app.py                          # Streamlit web dashboard
├── run_dashboard.py                # Dashboard launcher
├── biathlon_analysis.py            # Main data analysis
├── qualification_checker.py        # Olympic qualification system
├── run_analysis.py                 # Complete pipeline runner
├── requirements.txt                # Python dependencies
├── Results_Test_Version.csv        # Biathlon results dataset
├── Biathlon_Hauptkriterien.txt     # Qualification criteria
├── Task_description.pdf            # Project requirements
└── cleaned_biathlon_results.csv    # Processed dataset (generated)
```

## 📊 Current Results Summary

- **Total Athletes Analyzed**: 14 Swiss biathlon athletes
- **Qualified Athletes**: 8 (4 men, 4 women)
- **Qualification Rate**: 57.1%
- **Total Race Results**: 363 biathlon results analyzed
- **Date Range**: December 2024 - March 2026

### 🏆 Qualified Athletes
- **Women**: Amy Baserga, Lena Häcki-Groß, Aita Gasparin, Elisa Gasparin
- **Men**: Niklas Hartweg, Joscha Burkhalter, Sebastian Stalder, Jeremy Finello

## 🛠️ Technical Requirements

- **Python**: 3.8+
- **Key Dependencies**:
  - pandas >= 2.0.0
  - streamlit >= 1.28.0
  - plotly >= 5.15.0
  - numpy >= 1.20.0

## 🚀 Usage Examples

### View Team Overview
```bash
python run_dashboard.py
# Navigate to "📊 Overview" tab
```

### Analyze Specific Athlete
```bash
python run_dashboard.py
# Go to "👥 Athletes" tab
# Select athlete from dropdown
```

### Check Qualification Status
```bash
python qualification_checker.py
# Outputs detailed qualification report
```

## 📱 Dashboard Pages

1. **📊 Overview**: Team statistics and qualification summary
2. **👥 Athletes**: Individual athlete profiles and filtering
3. **📈 Performance Analysis**: Interactive charts and trends
4. **📋 Qualification Details**: Route explanations and breakdowns

## 🔧 Troubleshooting

### Dashboard won't start?
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Missing data files?
Ensure all CSV and criteria files are in the project directory.

### Import errors?
```bash
pip install --upgrade streamlit plotly pandas
```

## 📈 Future Enhancements

- [ ] Real-time data updates
- [ ] Export functionality for reports
- [ ] Mobile-responsive design
- [ ] Additional visualization options
- [ ] Athlete comparison tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for Swiss Olympic team selection analysis.

---

**🏔️ For the 2026 Milano Cortina Olympics** 🇨🇭
