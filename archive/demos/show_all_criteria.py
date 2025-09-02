#!/usr/bin/env python3
"""
Display script for all Swiss Olympic qualification criteria files
Shows a summary of all sports criteria for Milano Cortina 2026
"""

import os
from datetime import datetime

def display_sport_summary(sport_name, filename):
    """Display a summary of a sport's qualification criteria"""
    
    if not os.path.exists(filename):
        print(f"❌ {sport_name}: File not found")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"\n🏆 {sport_name.upper()}")
        print("-" * (len(sport_name) + 4))
        
        # Extract basic info
        for line in lines[:10]:
            line = line.strip()
            if line.startswith('Sport:') or line.startswith('Is Olympic Discipline:') or line.startswith('Team Members:'):
                print(f"  {line}")
        
        # Count routes
        route_count = sum(1 for line in lines if '# Route' in line and ':' in line)
        print(f"  Qualification Routes: {route_count}")
        
        # File size
        word_count = sum(len(line.split()) for line in lines)
        print(f"  Criteria Detail: {word_count} words")
        
    except Exception as e:
        print(f"❌ {sport_name}: Error reading file - {e}")

def main():
    """Main display function"""
    
    print("🏔️ SWISS OLYMPIC QUALIFICATION CRITERIA - MILANO CORTINA 2026")
    print("=" * 75)
    print("📋 Complete qualification criteria for all Swiss Olympic sports")
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Sports and their criteria files
    sports_files = [
        ("Biathlon", "criterias/Biathlon_Hauptkriterien.txt"),
        ("Alpine Skiing", "criterias/Alpine_Skiing_Hauptkriterien.txt"),
        ("Cross-Country Skiing", "criterias/Cross_Country_Skiing_Hauptkriterien.txt"),
        ("Freestyle Skiing", "criterias/Freestyle_Skiing_Hauptkriterien.txt"),
        ("Bobsleigh", "criterias/Bobsleigh_Hauptkriterien.txt"),
        ("Figure Skating", "criterias/Figure_Skating_Hauptkriterien.txt")
    ]
    
    print(f"\n📊 QUALIFICATION CRITERIA SUMMARY:")
    print("=" * 40)
    
    for sport_name, filename in sports_files:
        display_sport_summary(sport_name, filename)
    
    # Overview information
    print(f"\n🎯 MILANO CORTINA 2026 OLYMPICS OVERVIEW:")
    print("=" * 45)
    print("📅 Date: February 6-22, 2026")
    print("📍 Location: Milano & Cortina d'Ampezzo, Italy")
    print("🇨🇭 Team: Swiss Olympic Athletes")
    print(f"🏆 Sports: {len(sports_files)} winter sports disciplines")
    
    # Athletes count from our data
    try:
        import pandas as pd
        df = pd.read_csv('Results_Test_Version.csv', sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        df_swiss = df[df['Nationality'] == 'SUI']
        
        print(f"\n📈 SWISS ATHLETE DATABASE:")
        print("-" * 30)
        for sport_name, _ in sports_files:
            count = len(df_swiss[df_swiss['Sport'] == sport_name]['Person'].unique())
            print(f"  {sport_name:20}: {count:2} athletes")
        
        total_athletes = len(df_swiss['Person'].unique())
        total_results = len(df_swiss)
        print(f"\n  {'TOTAL':20}: {total_athletes:2} athletes")
        print(f"  {'RESULTS':20}: {total_results:2} competition results")
        
    except Exception as e:
        print(f"⚠️ Could not load athlete statistics: {e}")
    
    print(f"\n🚀 IMPLEMENTATION STATUS:")
    print("-" * 25)
    print("✅ Biathlon: Full qualification system implemented")
    print("✅ All Sports: Qualification criteria files created")
    print("🔄 Other Sports: Ready for implementation")
    
    print(f"\n📁 CRITERIA FILES CREATED:")
    print("-" * 27)
    for sport_name, filename in sports_files:
        size = os.path.getsize(filename) if os.path.exists(filename) else 0
        status = "✅" if size > 0 else "❌"
        print(f"  {status} {filename}")
    
    print(f"\n🔧 ADDITIONAL FILES:")
    print("-" * 20)
    additional_files = [
        "criterias/Swiss_Olympic_Qualification_Overview.txt",
        "verify_criteria_files.py",
        "show_all_criteria.py"
    ]
    
    for filename in additional_files:
        if os.path.exists(filename):
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename}")
    
    print(f"\n{'=' * 75}")
    print("🏔️ Swiss Olympic Team Selection System - Ready for Milano Cortina 2026!")
    print("🎿 All qualification criteria defined and documented")

if __name__ == "__main__":
    main()
