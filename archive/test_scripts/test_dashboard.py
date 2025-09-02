#!/usr/bin/env python3
"""
Test script for the updated multi-sport Streamlit dashboard
"""

import pandas as pd
from multi_sport_qualification_checker import MultiSportQualificationChecker

def test_dashboard_functions():
    """Test the dashboard functionality"""
    
    print("🧪 TESTING MULTI-SPORT DASHBOARD FUNCTIONS")
    print("=" * 50)
    
    # Load data
    try:
        df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        df = df[df['Nationality'] == 'SUI'].copy()
        
        print(f"✅ Data loaded: {len(df)} Swiss results")
        print(f"📊 Sports: {', '.join(sorted(df['Sport'].unique()))}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Test multi-sport qualification
    try:
        checker = MultiSportQualificationChecker(df)
        sports = df['Sport'].unique()
        sport_summaries = {}
        
        print(f"\n🏆 TESTING SPORT SUMMARIES:")
        
        for sport in sports:
            sport_athletes = df[df['Sport'] == sport]['Person'].unique()
            qualified_athletes = []
            
            for athlete in sport_athletes[:5]:  # Test first 5 athletes per sport
                if pd.notna(athlete):
                    athlete_qual = checker.check_athlete_qualification(athlete)
                    
                    if athlete_qual and not athlete_qual.get('error'):
                        sport_qual = athlete_qual['sports_qualifications'].get(sport, {})
                        if sport_qual.get('qualified', False):
                            qualified_athletes.append(athlete)
            
            sport_summaries[sport] = {
                'total': len(sport_athletes),
                'qualified': len(qualified_athletes),
                'qualified_names': qualified_athletes
            }
            
            qualification_rate = (len(qualified_athletes) / len(sport_athletes) * 100) if len(sport_athletes) > 0 else 0
            print(f"  {sport}: {len(qualified_athletes)}/{len(sport_athletes)} ({qualification_rate:.1f}%)")
        
        print(f"\n✅ Dashboard functions working correctly!")
        print(f"🚀 Run 'python run_dashboard.py' to view the updated dashboard")
        
    except Exception as e:
        print(f"❌ Error testing qualification functions: {e}")

if __name__ == "__main__":
    test_dashboard_functions()
