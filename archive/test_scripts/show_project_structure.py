#!/usr/bin/env python3
"""
Display the complete project structure for Swiss Olympic Biathlon Analysis System
Shows organized file structure with criterias folder
"""

import os
from datetime import datetime

def show_folder_contents(folder_path, title, description=""):
    """Display contents of a folder with details"""
    
    print(f"\n📁 {title}")
    print("=" * (len(title) + 4))
    if description:
        print(f"📝 {description}")
    
    if not os.path.exists(folder_path):
        print("❌ Folder not found")
        return
    
    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            files.append((item, size))
    
    if not files:
        print("📂 Empty folder")
        return
    
    # Sort files by name
    files.sort()
    
    total_size = 0
    for filename, size in files:
        total_size += size
        size_kb = size / 1024
        print(f"  📄 {filename:<40} ({size_kb:.1f} KB)")
    
    print(f"\n  📊 Total: {len(files)} files, {total_size/1024:.1f} KB")

def main():
    """Main display function"""
    
    print("🏔️ SWISS OLYMPIC BIATHLON ANALYSIS SYSTEM - PROJECT STRUCTURE")
    print("=" * 75)
    print("📋 Milano Cortina 2026 Olympics - Complete File Organization")
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Main project files
    print(f"\n🎯 MAIN PROJECT FILES")
    print("=" * 25)
    
    main_files = [
        ("biathlon_analysis.py", "Main data analysis engine"),
        ("qualification_checker.py", "Olympic qualification system"),
        ("athlete_lookup.py", "Interactive athlete search system"),
        ("app.py", "Analytics dashboard"),
        ("run_analysis.py", "Complete pipeline runner"),
        ("run_lookup.py", "Athlete lookup launcher"),
        ("run_dashboard.py", "Dashboard launcher")
    ]
    
    for filename, description in main_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  ✅ {filename:<30} | {description} ({size:.1f} KB)")
        else:
            print(f"  ❌ {filename:<30} | {description} (missing)")
    
    # Data files
    print(f"\n📊 DATA FILES")
    print("=" * 15)
    
    data_files = [
        ("Results_Test_Version.csv", "Competition results dataset"),
        ("cleaned_biathlon_results.csv", "Processed biathlon data"),
        ("Task_description.pdf", "Project requirements")
    ]
    
    for filename, description in data_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  📈 {filename:<30} | {description} ({size:.1f} KB)")
        else:
            print(f"  ❌ {filename:<30} | {description} (missing)")
    
    # Criterias folder
    show_folder_contents("criterias", "CRITERIAS FOLDER", 
                        "Olympic qualification criteria for all sports")
    
    # Setup and verification files
    print(f"\n🔧 SETUP & VERIFICATION")
    print("=" * 25)
    
    setup_files = [
        ("requirements.txt", "Python dependencies"),
        ("setup_info.md", "Setup documentation"),
        ("verify_setup.py", "System verification"),
        ("verify_criteria_files.py", "Criteria files checker"),
        ("verify_qualification.py", "Qualification verification"),
        ("show_all_criteria.py", "Criteria display tool")
    ]
    
    for filename, description in setup_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  🛠️  {filename:<30} | {description} ({size:.1f} KB)")
        else:
            print(f"  ❌ {filename:<30} | {description} (missing)")
    
    # Demo and test files
    print(f"\n🎮 DEMO & TEST FILES")
    print("=" * 22)
    
    demo_files = [
        ("demo_dashboard.py", "Dashboard demo"),
        ("demo_milano2026.py", "Milano 2026 features demo"),
        ("test_lookup.py", "Lookup system test guide"),
        ("show_project_structure.py", "This structure display script")
    ]
    
    for filename, description in demo_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  🎯 {filename:<30} | {description} ({size:.1f} KB)")
        else:
            print(f"  ❌ {filename:<30} | {description} (missing)")
    
    # Project statistics
    print(f"\n📊 PROJECT STATISTICS")
    print("=" * 22)
    
    # Count files
    total_files = 0
    total_size = 0
    
    # Main directory
    for item in os.listdir('.'):
        if os.path.isfile(item):
            total_files += 1
            total_size += os.path.getsize(item)
    
    # Criterias directory
    if os.path.exists('criterias'):
        for item in os.listdir('criterias'):
            item_path = os.path.join('criterias', item)
            if os.path.isfile(item_path):
                total_files += 1
                total_size += os.path.getsize(item_path)
    
    print(f"  📁 Total Files: {total_files}")
    print(f"  💾 Total Size: {total_size/1024:.1f} KB ({total_size/1024/1024:.2f} MB)")
    print(f"  🏔️ Sports Covered: 6 (Biathlon, Alpine, Cross-Country, Freestyle, Bobsleigh, Figure Skating)")
    print(f"  🏃‍♂️ Athletes: 177 Swiss Olympic athletes")
    print(f"  📈 Results: 2,349 competition results")
    
    # Key features
    print(f"\n🚀 KEY FEATURES")
    print("=" * 16)
    print("  ✅ Interactive athlete lookup system")
    print("  ✅ Milano Cortina 2026 qualification checking")
    print("  ✅ Multi-sport analysis (6 winter sports)")
    print("  ✅ Web-based dashboards and analytics")
    print("  ✅ Organized qualification criteria system")
    print("  ✅ Complete verification and testing suite")
    
    print(f"\n{'=' * 75}")
    print("🏔️ Swiss Olympic Team Selection System - Milano Cortina 2026")
    print("🎿 Complete project structure organized and ready for use!")

if __name__ == "__main__":
    main()
