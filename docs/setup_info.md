# Swiss Olympic Biathlon Analysis System - Setup Information

## 🏔️ Milano Cortina 2026 Olympics - Team Selection System

### 📋 Project Overview
This system analyzes Swiss biathlon athletes' performance and determines their qualification status for the 2026 Winter Olympics in Milano Cortina, Italy.

### 🔧 System Requirements

#### Python Version
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9 or higher
- **Tested on**: Python 3.12

#### Operating System Support
- ✅ macOS (tested on Darwin 24.2.0)
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+)

### 📦 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/Trista1208/swiss_winter_olympics.git
cd swiss_winter_olympics
```

#### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 🚀 Quick Start

#### Option 1: Interactive Athlete Lookup (Recommended)
```bash
python run_lookup.py
```
- Open: http://localhost:8502
- Search athletes by name
- Filter by sport and gender
- Check Milano 2026 qualification status

#### Option 2: Analytics Dashboard
```bash
python run_dashboard.py
```
- Open: http://localhost:8501
- View team statistics
- Performance analysis charts

#### Option 3: Command Line Analysis
```bash
python run_analysis.py
```

### 📊 Data Requirements

#### Input Files (Included)
- `Results_Test_Version.csv` - Competition results data
- `Biathlon_Hauptkriterien.txt` - Qualification criteria
- `Task_description.pdf` - Project requirements

#### Generated Files
- `cleaned_biathlon_results.csv` - Processed dataset
- Various analysis outputs

### 🎯 Key Features

#### Athlete Lookup System
- 177 Swiss Olympic athletes across 6 sports
- Milano 2026 qualification checking
- Interactive search and filtering
- Detailed athlete profiles

#### Qualification Analysis
- 5 Olympic qualification routes for biathlon
- Real-time status checking
- Route-by-route breakdown
- Team selection summary

#### Data Coverage
- **Sports**: Alpine Skiing, Biathlon, Bobsleigh, Cross-Country, Figure Skating, Freestyle
- **Time Period**: December 2024 - March 2026
- **Results**: 2,349 competition results
- **Focus**: Swiss biathlon team for Milano Cortina 2026

### 🔍 Troubleshooting

#### Common Issues

**Port Already in Use:**
```bash
# Kill existing processes
pkill -f "streamlit"
# Or use different ports
streamlit run app.py --server.port 8503
```

**Missing Dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Data Loading Issues:**
- Ensure CSV files are in project directory
- Check file encoding (should be UTF-8)
- Verify file permissions

### 📈 Performance Notes

#### System Resources
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: ~50MB for project files
- **Network**: Required for initial package installation

#### Optimization
- Data is cached using Streamlit's caching system
- Large datasets are processed efficiently with pandas
- Interactive components use session state for persistence

### 🏆 Milano Cortina 2026 Specific Information

#### Olympic Games Details
- **Date**: February 6-22, 2026
- **Location**: Milano Cortina, Italy
- **Focus Sport**: Biathlon team selection

#### Qualification Summary
- **Total Biathlon Athletes**: 14
- **Qualified for Milano 2026**: 8 (4 men, 4 women)
- **Qualification Rate**: 57.1%

#### Qualification Routes
1. Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26
2. 1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26
3. 1x Top-15 in World Cup 2025/26
4. 2x Top-25 in World Cup 2025/26
5. 1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26

### 📞 Support

For technical issues or questions about the system:
1. Check the README.md for detailed usage instructions
2. Review the demo scripts for examples
3. Ensure all requirements are properly installed

---

**🏔️ Swiss Olympic Team Analysis System**  
*Developed for Milano Cortina 2026 Winter Olympics Team Selection*
