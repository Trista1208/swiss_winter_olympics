# 🏔️ Swiss Olympic Multi-Sport Analysis System

A comprehensive analysis system for Swiss winter sport athletes' Olympic qualification for the 2026 Milano Cortina Olympics across 6 sports: Biathlon, Alpine Skiing, Cross-Country Skiing, Freestyle Skiing, Bobsleigh, and Figure Skating.

## 🚀 Quick Start

### Option 1: Multi-Sport Dashboard (Recommended)
```bash
python scripts/run_dashboard.py
```
**URL**: `http://localhost:8501`
- **🏆 Team Overview** - Overall statistics and progress
- **👥 Athletes by Sport** - All athlete names organized by sport categories  
- **📊 Sport Statistics** - Interactive charts and comparisons
- **📋 Qualification Routes** - Detailed criteria for each sport

### Option 2: Athlete Lookup System
```bash
python scripts/run_lookup.py
```
**URL**: `http://localhost:8502`
- **🔍 Search athletes** by name (type or select)
- **🏅 Filter by sport** and qualification status
- **📋 Detailed athlete profiles** with Milano 2026 qualification status

### Option 3: Command-Line Analysis
```bash
python scripts/run_analysis.py
```
Comprehensive terminal-based analysis across all sports

---

## 📊 Current Team Status (Milano Cortina 2026)

| Sport | Athletes | Qualified | Rate |
|-------|----------|-----------|------|
| **🛷 Bobsleigh** | 22 | 21 | **95.5%** |
| **🎯 Biathlon** | 14 | 8 | 57.1% |
| **🤸 Freestyle Skiing** | 49 | 25 | 51.0% |
| **🎿 Cross-Country Skiing** | 29 | 14 | 48.3% |
| **⛷️ Alpine Skiing** | 57 | 25 | 43.9% |
| **⛸️ Figure Skating** | 6 | 0 | 0.0% |
| **🇨🇭 TOTAL** | **177** | **93** | **52.5%** |

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Trista1208/swiss_winter_olympics.git
cd swiss_winter_olympics
```

2. **Install requirements**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
python scripts/run_dashboard.py
```

---

## 📁 Project Structure

```
swiss_Olympics/
├── 📋 requirements.txt          # Python dependencies
├── 📖 README.md                 # Project documentation
├── 
├── 📂 scripts/                  # Launcher scripts
│   ├── run_dashboard.py         # Launch main dashboard
│   ├── run_lookup.py            # Launch athlete search
│   └── run_analysis.py          # Command-line analysis
├── 
├── 📂 src/                      # Source code
│   ├── app.py                   # Main dashboard app
│   ├── athlete_lookup.py        # Athlete search interface
│   ├── multi_sport_analysis.py  # Multi-sport analysis
│   ├── multi_sport_qualification_checker.py  # Qualification logic
│   ├── biathlon_analysis.py     # Biathlon-specific analysis
│   └── qualification_checker.py # Biathlon qualification checker
├── 
├── 📂 data/                     # Data files
│   ├── Results_Test_Version.csv # Main dataset
│   ├── Task_description.pdf    # Project requirements
│   └── cleaned_biathlon_results.csv
├── 
├── 📂 criterias/               # Qualification criteria
│   ├── Biathlon_Hauptkriterien.txt
│   ├── Alpine_Skiing_Hauptkriterien.txt
│   ├── Cross_Country_Skiing_Hauptkriterien.txt
│   ├── Freestyle_Skiing_Hauptkriterien.txt
│   ├── Bobsleigh_Hauptkriterien.txt
│   └── Figure_Skating_Hauptkriterien.txt
├── 
├── 📂 docs/                    # Documentation
│   ├── setup_info.md
│   └── implementation_summaries/
├── 
└── 📂 archive/                 # Archived files
    ├── old_versions/
    ├── test_scripts/
    └── demos/
```

---

## 🎯 Features

### **Multi-Sport Analysis**
- ✅ **6 Winter Sports** covered with individual qualification criteria
- ✅ **177 Swiss Athletes** tracked across all sports  
- ✅ **5 Qualification Routes** per sport (30 total routes)
- ✅ **Real-time Status** for Milano Cortina 2026

### **Interactive Dashboards**
- ✅ **Highly visible design** with animations and gradients
- ✅ **Sport-by-sport breakdown** with athlete names
- ✅ **Individual athlete cards** showing qualification routes
- ✅ **Interactive charts** and statistics
- ✅ **Search and filtering** capabilities

### **Qualification System**
- ✅ **Sport-specific criteria** (each sport treated separately)
- ✅ **Route-based qualification** (5 routes per sport)
- ✅ **Milano 2026 focused** qualification tracking
- ✅ **Swiss Olympic standards** implementation

---

## 🏅 Qualification Highlights

### **Top Qualified Athletes by Sport:**

**🛷 Bobsleigh (21/22 qualified)**
- Michael Vogt, Melanie Hasler, Andreas Haas, Gregory Jones

**🎯 Biathlon (8/14 qualified)**  
- Amy Baserga, Lena Häcki-Groß, Niklas Hartweg, Aita Gasparin

**🤸 Freestyle Skiing (25/49 qualified)**
- Andri Ragettli, Mathilde Gremaud, Sarah Hoefflin, Noe Roth

**🎿 Cross-Country Skiing (14/29 qualified)**
- Nadja Kälin, Nadine Fähndrich, Jason Rüesch, Jonas Baumann

**⛷️ Alpine Skiing (25/57 qualified)**
- Marco Odermatt, Lara Gut-Behrami, Loïc Meillard, Wendy Holdener

---

## 🔧 Technical Details

- **Framework**: Streamlit for web interfaces
- **Analysis**: Pandas, NumPy for data processing  
- **Visualization**: Plotly for interactive charts
- **Data**: 2,349+ Swiss athlete results
- **Qualification Logic**: Custom multi-sport checker system

---

## 🚀 Getting Started

1. **View Team Overview**: `python scripts/run_dashboard.py` → "🏆 Team Overview"
2. **Browse Athletes**: Navigate to "👥 Athletes by Sport" 
3. **Search Individual Athletes**: `python scripts/run_lookup.py`
4. **View Qualification Criteria**: Dashboard → "📋 Qualification Routes"

**Perfect for presentations, team analysis, and Milano 2026 Olympic preparation!** 🏔️✨