# 🏔️ Swiss Olympic Multi-Sport System - Quick Start

## 🚀 **Immediate Usage**

### **1. Launch Main Dashboard** (Recommended)
```bash
python scripts/run_dashboard.py
```
- **URL**: `http://localhost:8501`
- **View**: All 177 Swiss athletes organized by sport categories
- **Features**: Team overview, athlete names by sport, qualification status

### **2. Launch Athlete Search**
```bash
python scripts/run_lookup.py
```
- **URL**: `http://localhost:8502`
- **Search**: Individual athletes by name
- **Filter**: By sport and qualification status

### **3. Command-Line Analysis**
```bash
python scripts/run_analysis.py
```
- **Output**: Terminal-based comprehensive analysis
- **Shows**: All qualified athletes across all 6 sports

---

## 📊 **What You'll See**

### **Dashboard Sections:**
1. **🏆 Team Overview** - Overall statistics (93 qualified / 177 total)
2. **👥 Athletes by Sport** - All athlete names organized by categories
3. **📊 Sport Statistics** - Interactive charts and comparisons
4. **📋 Qualification Routes** - Detailed criteria for each sport

### **Sports Covered:**
- **🛷 Bobsleigh** - 21/22 qualified (95.5%)
- **🎯 Biathlon** - 8/14 qualified (57.1%)
- **🤸 Freestyle Skiing** - 25/49 qualified (51.0%)
- **🎿 Cross-Country Skiing** - 14/29 qualified (48.3%)
- **⛷️ Alpine Skiing** - 25/57 qualified (43.9%)
- **⛸️ Figure Skating** - 0/6 qualified (0.0%)

---

## 🎯 **Key Features**

✅ **Individual Athlete Names** - Every athlete listed by sport category  
✅ **Qualification Status** - Clear ✅/❌ indicators for Milano 2026  
✅ **Qualification Routes** - Which specific routes each athlete qualified through  
✅ **Highly Visible UI** - Modern design with animations and gradients  
✅ **Interactive Search** - Find athletes by name across all sports  
✅ **Real-time Statistics** - Live qualification tracking  

---

## 📁 **Clean Project Structure**

```
swiss_Olympics/
├── 📋 requirements.txt         # Dependencies
├── 📖 README.md               # Full documentation
├── 
├── 📂 scripts/                # Launcher scripts
│   ├── run_dashboard.py       # Main dashboard
│   ├── run_lookup.py          # Athlete search
│   └── run_analysis.py        # Command analysis
├── 
├── 📂 src/                    # Source code
├── 📂 data/                   # Data files
├── 📂 criterias/             # Qualification criteria
├── 📂 docs/                   # Documentation
└── 📂 archive/                # Archived files
```

---

## ⚡ **Installation** (If needed)
```bash
pip install -r requirements.txt
```

**That's it! The system is ready to use immediately.** 🏔️✨
