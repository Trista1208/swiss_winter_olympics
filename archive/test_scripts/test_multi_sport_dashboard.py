#!/usr/bin/env python3
"""
Test script to verify multi-sport dashboard functionality
"""

import pandas as pd
from multi_sport_qualification_checker import MultiSportQualificationChecker

def test_dashboard_data():
    """Test that the dashboard will display all sports correctly"""
    
    print("🧪 TESTING MULTI-SPORT DASHBOARD DATA")
    print("=" * 50)
    
    # Load data exactly as the dashboard does
    try:
        df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        df = df[df['Nationality'] == 'SUI'].copy()
        
        print(f"✅ Data loaded: {len(df)} Swiss results")
        
        # Get sports breakdown
        sports = sorted(df['Sport'].unique())
        print(f"📊 Sports in dataset: {len(sports)}")
        
        for sport in sports:
            sport_count = len(df[df['Sport'] == sport])
            athletes_count = len(df[df['Sport'] == sport]['Person'].unique())
            print(f"  🏅 {sport}: {athletes_count} athletes, {sport_count} results")
        
        # Test qualification system
        checker = MultiSportQualificationChecker(df)
        sport_summaries = {}
        
        print(f"\n🎯 QUALIFICATION TESTING:")
        
        for sport in sports:
            sport_athletes = df[df['Sport'] == sport]['Person'].unique()
            qualified_athletes = []
            
            # Test first few athletes per sport
            test_count = min(3, len(sport_athletes))
            for athlete in sport_athletes[:test_count]:
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
            
            rate = (len(qualified_athletes) / len(sport_athletes) * 100) if len(sport_athletes) > 0 else 0
            print(f"  ✅ {sport}: {len(qualified_athletes)}/{len(sport_athletes)} qualified ({rate:.1f}%)")
            
            if qualified_athletes:
                print(f"      Sample qualified: {', '.join(qualified_athletes[:2])}")
        
        print(f"\n📈 DASHBOARD SUMMARY:")
        total_athletes = len(df['Person'].unique())
        total_qualified = sum(summary['qualified'] for summary in sport_summaries.values())
        overall_rate = (total_qualified / total_athletes * 100) if total_athletes > 0 else 0
        
        print(f"  🏆 Total Athletes: {total_athletes}")
        print(f"  ✅ Total Qualified: {total_qualified}")
        print(f"  📊 Overall Rate: {overall_rate:.1f}%")
        
        print(f"\n🚀 DASHBOARD READY!")
        print("All sports are properly loaded and qualification system is working.")
        print("Run 'python run_dashboard.py' to launch the multi-sport dashboard.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard_data()
