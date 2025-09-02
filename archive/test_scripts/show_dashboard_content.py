#!/usr/bin/env python3
"""
Show what the multi-sport dashboard displays
"""

import pandas as pd
from multi_sport_qualification_checker import MultiSportQualificationChecker

def main():
    """Show dashboard content preview"""
    
    print("🏔️ SWISS OLYMPIC MULTI-SPORT DASHBOARD PREVIEW")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
    df.columns = df.columns.str.strip('"')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
    df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
    df = df[df['Nationality'] == 'SUI'].copy()
    
    # Get qualification results
    checker = MultiSportQualificationChecker(df)
    qualification_results = {}
    sport_summaries = {}
    
    sports = df['Sport'].unique()
    
    for sport in sports:
        sport_athletes = df[df['Sport'] == sport]['Person'].unique()
        qualified_athletes = []
        
        for athlete in sport_athletes:
            if pd.notna(athlete):
                athlete_qual = checker.check_athlete_qualification(athlete)
                
                if athlete_qual and not athlete_qual.get('error'):
                    sport_qual = athlete_qual['sports_qualifications'].get(sport, {})
                    if sport_qual.get('qualified', False):
                        qualified_athletes.append(athlete)
                        qualification_results[athlete] = athlete_qual
        
        sport_summaries[sport] = {
            'total': len(sport_athletes),
            'qualified': len(qualified_athletes),
            'qualified_names': qualified_athletes
        }
    
    # Display what the dashboard shows
    print("\n🏆 TEAM OVERVIEW SECTION:")
    print("-" * 40)
    
    total_athletes = len(df['Person'].unique())
    total_qualified = len(qualification_results)
    qualification_rate = (total_qualified / total_athletes * 100) if total_athletes > 0 else 0
    
    print(f"🇨🇭 Total Athletes: {total_athletes}")
    print(f"✅ Qualified: {total_qualified}")
    print(f"⏳ Pending: {total_athletes - total_qualified}")
    print(f"📈 Success Rate: {qualification_rate:.1f}%")
    
    print("\n📊 SPORT-BY-SPORT ANALYSIS:")
    print("-" * 40)
    
    for sport, summary in sport_summaries.items():
        rate = (summary['qualified'] / summary['total'] * 100) if summary['total'] > 0 else 0
        status = "✅ QUALIFIED" if summary['qualified'] > 0 else "❌ NO QUALIFICATIONS"
        
        # Get sport emoji
        sport_emojis = {
            'Biathlon': '🎯',
            'Alpine Skiing': '⛷️',
            'Cross-Country Skiing': '🎿',
            'Freestyle Skiing': '🤸',
            'Bobsleigh': '🛷',
            'Figure Skating': '⛸️'
        }
        emoji = sport_emojis.get(sport, '🏔️')
        
        print(f"\n{emoji} {sport.upper()}")
        print(f"   Athletes: {summary['total']}")
        print(f"   Qualified: {summary['qualified']}")
        print(f"   Rate: {rate:.1f}%")
        print(f"   Status: {status}")
        
        if summary['qualified'] > 0:
            qualified_sample = summary['qualified_names'][:3]  # Show first 3
            print(f"   Sample: {', '.join(qualified_sample)}")
            if len(summary['qualified_names']) > 3:
                print(f"           (+{len(summary['qualified_names'])-3} more)")
    
    print("\n👥 ATHLETE PROFILES SECTION:")
    print("-" * 40)
    print("Available filters:")
    print("  - All Sports / Individual Sport Selection")
    print("  - All / Qualified / Not Qualified")
    print(f"Total searchable athletes: {total_athletes}")
    
    print("\n📋 QUALIFICATION ROUTES SECTION:")
    print("-" * 40)
    print("Available sports for detailed criteria:")
    for sport in sorted(sports):
        emoji = sport_emojis.get(sport, '🏔️')
        print(f"  {emoji} {sport} - 5 qualification routes")
    
    print(f"\n🚀 ACCESS INFORMATION:")
    print("-" * 40)
    print("Dashboard URL: http://localhost:8501")
    print("Launch command: python run_dashboard.py")
    print("\nSections available:")
    print("  1. 🏆 Team Overview - Overall statistics and progress")
    print("  2. 📊 Sport Analysis - Sport-by-sport breakdown with charts")
    print("  3. 👥 Athlete Profiles - Individual athlete search and filtering")
    print("  4. 📋 Qualification Routes - Detailed criteria for each sport")
    
    print(f"\n✨ FEATURES:")
    print("  ✅ Animated gradient headers and backgrounds")
    print("  ✅ 3D hover effects on cards")
    print("  ✅ Interactive sport cards with qualification status")
    print("  ✅ Real-time progress bars")
    print("  ✅ Sport-specific emojis and color coding")
    print("  ✅ High contrast, highly visible design")

if __name__ == "__main__":
    main()
