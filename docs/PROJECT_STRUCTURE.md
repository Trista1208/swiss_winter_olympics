# 🏔️ Swiss Olympic Team Selection System - Project Structure

## 📁 Directory Overview

```
swiss_Olympics/
├── 📊 src/                          # Core application source code
│   ├── app.py                       # Main Streamlit dashboard (BLACK THEME)
│   ├── athlete_lookup.py            # Interactive athlete search tool
│   ├── multi_sport_qualification_checker.py  # Core qualification logic
│   ├── multi_sport_analysis.py     # Command-line analysis tool
│   ├── biathlon_analysis.py        # Legacy biathlon-specific analysis
│   └── qualification_checker.py    # Legacy biathlon qualification checker
│
├── 🚀 scripts/                      # Launcher scripts
│   ├── run_dashboard.py            # Launch main dashboard
│   ├── run_lookup.py               # Launch athlete lookup tool
│   ├── run_analysis.py             # Run comprehensive analysis
│   └── project_structure.py        # Display project structure
│
├── 📋 criterias/                    # Olympic qualification criteria
│   ├── Biathlon_Hauptkriterien.txt
│   ├── Alpine_Skiing_Hauptkriterien.txt
│   ├── Cross_Country_Skiing_Hauptkriterien.txt
│   ├── Freestyle_Skiing_Hauptkriterien.txt
│   ├── Bobsleigh_Hauptkriterien.txt
│   ├── Figure_Skating_Hauptkriterien.txt
│   ├── Swiss_Olympic_Qualification_Overview.txt
│   └── README.md
│
├── 📁 data/                         # Competition results and task files
│   ├── Results_Test_Version.csv    # Main competition dataset (semicolon-delimited)
│   ├── Results_Test_Version.xlsx   # Excel version of results
│   ├── cleaned_biathlon_results.csv # Processed biathlon data
│   └── Task_description.pdf        # Original project requirements
│
├── 📚 docs/                         # Documentation and summaries
│   ├── README.md                   # Main project documentation
│   ├── PROJECT_STRUCTURE.md       # This file - project organization
│   ├── setup_info.md              # Installation and setup guide
│   ├── MULTI_SPORT_IMPLEMENTATION_SUMMARY.md  # Multi-sport development log
│   ├── STREAMLIT_UPDATE_SUMMARY.md # Dashboard enhancement log
│   └── UI_REDESIGN_SUMMARY.md     # UI/UX design evolution
│
├── 📦 archive/                      # Historical versions and tests
│   ├── old_versions/               # Previous app versions
│   │   ├── app_broken.py
│   │   ├── app_final.py
│   │   ├── app_new.py
│   │   ├── app_old.py
│   │   └── app_old_complex.py
│   ├── test_scripts/              # Development and testing scripts
│   │   └── [various test files]
│   ├── demos/                     # Demo and example scripts
│   │   └── [demo files]
│   └── documentation/             # Archived documentation
│
├── 🔧 Configuration Files
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                # Git ignore rules (updated)
│   ├── README.md                 # Project overview
│   └── QUICK_START.md            # Quick start guide
```

## 🎯 Key Components

### 🖤 Main Dashboard (`src/app.py`)
- **Black theme** with maximum visibility
- **177+ Swiss athletes** with complete profiles
- **6 winter sports** qualification tracking
- **Milano Cortina 2026** Olympic preparation
- Advanced filtering and search capabilities

### 🔍 Athlete Lookup (`src/athlete_lookup.py`)
- Interactive athlete search and filtering
- Detailed individual athlete profiles
- Competition history and performance metrics
- Qualification status by sport

### ⚙️ Qualification Engine (`src/multi_sport_qualification_checker.py`)
- **5 qualification routes** per sport
- **6 winter sports** supported:
  - Biathlon
  - Alpine Skiing
  - Cross-Country Skiing
  - Freestyle Skiing
  - Bobsleigh
  - Figure Skating

## 🚀 Quick Start

```bash
# Launch main dashboard
python scripts/run_dashboard.py

# Launch athlete lookup tool
python scripts/run_lookup.py

# Run comprehensive analysis
python scripts/run_analysis.py
```

## 📊 Data Flow

1. **Raw Data** (`data/Results_Test_Version.csv`)
2. **Qualification Logic** (`criterias/*.txt`)
3. **Processing Engine** (`src/multi_sport_qualification_checker.py`)
4. **User Interface** (`src/app.py` + `src/athlete_lookup.py`)
5. **Analysis & Reports** (`src/multi_sport_analysis.py`)

## 🎨 UI Features

- **🖤 Black Theme** - High contrast, maximum visibility
- **👤 Athlete Profiles** - Comprehensive individual analysis
- **🏅 Qualification Tracking** - Milano 2026 Olympic status
- **📈 Performance Metrics** - Competition statistics
- **🔍 Smart Search** - Instant athlete filtering
- **📊 Team Overview** - Sport-by-sport summaries

## 🔄 Version History

All previous versions and development iterations are preserved in the `archive/` directory for reference and rollback capabilities.

---

**Swiss Olympic Team Selection System** - Milano Cortina 2026 🏔️✨
