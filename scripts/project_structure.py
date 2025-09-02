#!/usr/bin/env python3
"""
Show clean project structure after organization
"""

import os

def show_structure():
    """Display the organized project structure"""
    
    print("🏔️ SWISS OLYMPIC PROJECT - CLEAN STRUCTURE")
    print("=" * 55)
    
    structure = {
        "📊 Main Launchers": [
            "run_dashboard.py - Launch multi-sport dashboard",
            "run_lookup.py - Launch athlete search interface", 
            "run_analysis.py - Command-line analysis",
            "requirements.txt - Python dependencies",
            "README.md - Project documentation"
        ],
        "📂 src/ (Source Code)": [
            "app.py - Main dashboard application",
            "athlete_lookup.py - Athlete search interface",
            "multi_sport_analysis.py - Multi-sport analysis engine",
            "multi_sport_qualification_checker.py - Qualification logic",
            "biathlon_analysis.py - Biathlon-specific analysis",
            "qualification_checker.py - Biathlon qualification checker"
        ],
        "📂 data/ (Data Files)": [
            "Results_Test_Version.csv - Main dataset (2,349+ results)",
            "Task_description.pdf - Project requirements",
            "cleaned_biathlon_results.csv - Processed biathlon data"
        ],
        "📂 criterias/ (Qualification Criteria)": [
            "Biathlon_Hauptkriterien.txt",
            "Alpine_Skiing_Hauptkriterien.txt", 
            "Cross_Country_Skiing_Hauptkriterien.txt",
            "Freestyle_Skiing_Hauptkriterien.txt",
            "Bobsleigh_Hauptkriterien.txt",
            "Figure_Skating_Hauptkriterien.txt",
            "Swiss_Olympic_Qualification_Overview.txt"
        ],
        "📂 docs/ (Documentation)": [
            "README.md - Main project documentation",
            "setup_info.md - Installation guide",
            "MULTI_SPORT_IMPLEMENTATION_SUMMARY.md",
            "STREAMLIT_UPDATE_SUMMARY.md",
            "UI_REDESIGN_SUMMARY.md"
        ],
        "📂 archive/ (Archived Files)": [
            "old_versions/ - Previous app versions",
            "test_scripts/ - Testing and verification scripts",
            "demos/ - Demo and example scripts"
        ]
    }
    
    for category, files in structure.items():
        print(f"\n{category}")
        print("-" * 40)
        for file in files:
            print(f"  {file}")
    
    print(f"\n🚀 QUICK START:")
    print("-" * 40)
    print("1. Install: pip install -r requirements.txt")
    print("2. Dashboard: python run_dashboard.py")
    print("3. Search: python run_lookup.py")
    print("4. Analysis: python run_analysis.py")
    
    print(f"\n📊 PROJECT STATS:")
    print("-" * 40)
    print("• 6 Winter Sports covered")
    print("• 177 Swiss Athletes tracked")
    print("• 93 Athletes qualified (52.5%)")
    print("• 30 Qualification routes (5 per sport)")
    print("• 2,349+ Competition results")
    
    print(f"\n✅ ORGANIZATION COMPLETE!")
    print("Clean, professional project structure ready for use.")

if __name__ == "__main__":
    show_structure()
