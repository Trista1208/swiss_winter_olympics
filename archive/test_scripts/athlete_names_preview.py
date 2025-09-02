#!/usr/bin/env python3
"""
Preview of athlete names organized by sport categories
Shows exactly what the dashboard displays
"""

import pandas as pd
from multi_sport_qualification_checker import MultiSportQualificationChecker

def main():
    """Show preview of athlete names by sport categories"""
    
    print("🏔️ SWISS OLYMPIC DASHBOARD - ATHLETE NAMES BY SPORT CATEGORIES")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
    df.columns = df.columns.str.strip('"')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
    df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
    df = df[df['Nationality'] == 'SUI'].copy()
    
    # Get qualification results
    checker = MultiSportQualificationChecker(df)
    sport_summaries = {}
    
    sports = df['Sport'].unique()
    
    for sport in sports:
        sport_athletes = df[df['Sport'] == sport]['Person'].unique()
        sport_athlete_details = {}
        qualified_count = 0
        
        for athlete in sport_athletes:
            if pd.notna(athlete):
                athlete_qual = checker.check_athlete_qualification(athlete)
                
                if athlete_qual and not athlete_qual.get('error'):
                    sport_qual = athlete_qual['sports_qualifications'].get(sport, {})
                    is_qualified = sport_qual.get('qualified', False)
                    qualified_routes = sport_qual.get('qualified_routes', [])
                    
                    sport_athlete_details[athlete] = {
                        'qualified': is_qualified,
                        'routes': qualified_routes
                    }
                    
                    if is_qualified:
                        qualified_count += 1
                else:
                    sport_athlete_details[athlete] = {
                        'qualified': False,
                        'routes': []
                    }
        
        sport_summaries[sport] = {
            'total': len(sport_athletes),
            'qualified': qualified_count,
            'all_athletes': sport_athlete_details
        }
    
    # Display each sport category with athlete names
    sport_emojis = {
        'Biathlon': '🎯',
        'Alpine Skiing': '⛷️',
        'Cross-Country Skiing': '🎿',
        'Freestyle Skiing': '🤸',
        'Bobsleigh': '🛷',
        'Figure Skating': '⛸️'
    }
    
    for sport in sorted(sport_summaries.keys()):
        emoji = sport_emojis.get(sport, '🏔️')
        data = sport_summaries[sport]
        qualification_rate = (data['qualified'] / data['total'] * 100) if data['total'] > 0 else 0
        
        print(f"\n{emoji} {sport.upper()}")
        print("-" * 50)
        print(f"Total Athletes: {data['total']} | Qualified: {data['qualified']} | Rate: {qualification_rate:.1f}%")
        print()
        
        # Sort athletes: qualified first, then alphabetically
        athletes = data['all_athletes']
        sorted_athletes = sorted(athletes.items(), key=lambda x: (not x[1]['qualified'], x[0]))
        
        qualified_athletes = []
        not_qualified_athletes = []
        
        for athlete_name, athlete_info in sorted_athletes:
            if athlete_info['qualified']:
                routes_str = f" (via {', '.join(athlete_info['routes'])})" if athlete_info['routes'] else ""
                qualified_athletes.append(f"✅ {athlete_name}{routes_str}")
            else:
                not_qualified_athletes.append(f"❌ {athlete_name}")
        
        # Display qualified athletes first
        if qualified_athletes:
            print("🏅 QUALIFIED ATHLETES:")
            for athlete in qualified_athletes:
                print(f"  {athlete}")
            print()
        
        # Display not qualified athletes
        if not_qualified_athletes:
            print("⏳ NOT YET QUALIFIED:")
            for athlete in not_qualified_athletes[:10]:  # Show first 10
                print(f"  {athlete}")
            if len(not_qualified_athletes) > 10:
                print(f"  ... and {len(not_qualified_athletes) - 10} more athletes")
            print()
        
        print("=" * 50)
    
    # Overall summary
    total_athletes = len(df['Person'].unique())
    total_qualified = sum(data['qualified'] for data in sport_summaries.values())
    overall_rate = (total_qualified / total_athletes * 100) if total_athletes > 0 else 0
    
    print(f"\n🇨🇭 OVERALL SWISS OLYMPIC TEAM SUMMARY")
    print("=" * 50)
    print(f"Total Swiss Athletes: {total_athletes}")
    print(f"Total Qualified: {total_qualified}")
    print(f"Overall Qualification Rate: {overall_rate:.1f}%")
    
    print(f"\n🚀 DASHBOARD ACCESS:")
    print("URL: http://localhost:8501")
    print("Navigate to: 👥 Athletes by Sport")
    print("Features:")
    print("  ✅ Individual athlete cards with qualification status")
    print("  ✅ Organized by sport categories")
    print("  ✅ Shows qualification routes for each athlete")
    print("  ✅ Visual distinction between qualified/not qualified")
    print("  ✅ Highly visible design with animations")

if __name__ == "__main__":
    main()
