#!/usr/bin/env python3
"""
Multi-Sport Qualification Analysis for Swiss Olympic Team Selection
Milano Cortina 2026 Olympics - Comprehensive Analysis Across All Sports

This script provides a complete overview of Swiss athlete qualification status
across all winter sports: Biathlon, Alpine Skiing, Cross-Country Skiing, 
Freestyle Skiing, Bobsleigh, and Figure Skating.
"""

import pandas as pd
from multi_sport_qualification_checker import MultiSportQualificationChecker

def main():
    """Run comprehensive multi-sport qualification analysis"""
    
    print("🏔️ SWISS OLYMPIC TEAM SELECTION ANALYSIS")
    print("Milano Cortina 2026 Winter Olympics")
    print("=" * 60)
    
    # Load data
    try:
        df = pd.read_csv("data/Results_Test_Version.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        df = df[df['Nationality'] == 'SUI'].copy()  # Swiss athletes only
        
        print(f"✅ Data loaded: {len(df)} Swiss results")
        print(f"📊 Sports covered: {', '.join(sorted(df['Sport'].unique()))}")
        print(f"👥 Total athletes: {len(df['Person'].unique())}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Initialize checker
    checker = MultiSportQualificationChecker(df)
    
    # Sport-by-sport analysis
    print(f"\n🎯 SPORT-BY-SPORT QUALIFICATION ANALYSIS")
    print("-" * 60)
    
    sport_summary = {}
    
    for sport in sorted(df['Sport'].unique()):
        sport_athletes = df[df['Sport'] == sport]['Person'].unique()
        qualified_athletes = []
        
        print(f"\n🏆 {sport.upper()}")
        print(f"Total athletes: {len(sport_athletes)}")
        
        for athlete in sport_athletes:
            if pd.notna(athlete):
                result = checker.check_athlete_qualification(athlete)
                
                if not result or 'error' in result:
                    continue
                
                sport_qual = result['sports_qualifications'].get(sport)
                if sport_qual and sport_qual.get('qualified', False):
                    qualified_athletes.append(athlete)
                    qualified_routes = sport_qual.get('qualified_routes', [])
                    print(f"  ✅ {athlete:<30} | {', '.join(qualified_routes)}")
        
        if not qualified_athletes:
            print(f"  ❌ No qualified athletes")
        
        sport_summary[sport] = {
            'total_athletes': len(sport_athletes),
            'qualified_athletes': len(qualified_athletes),
            'qualification_rate': len(qualified_athletes) / len(sport_athletes) * 100 if len(sport_athletes) > 0 else 0,
            'qualified_names': qualified_athletes
        }
        
        print(f"  📈 Qualification rate: {sport_summary[sport]['qualification_rate']:.1f}% ({len(qualified_athletes)}/{len(sport_athletes)})")
    
    # Overall summary
    print(f"\n📊 OVERALL MILANO CORTINA 2026 QUALIFICATION SUMMARY")
    print("=" * 60)
    
    total_qualified = 0
    total_athletes = len(df['Person'].unique())
    
    print(f"{'Sport':<20} {'Athletes':<10} {'Qualified':<10} {'Rate':<8} {'Names'}")
    print("-" * 80)
    
    for sport, data in sport_summary.items():
        total_qualified += data['qualified_athletes']
        names_str = ', '.join(data['qualified_names'][:3])  # Show first 3 names
        if len(data['qualified_names']) > 3:
            names_str += f" (+{len(data['qualified_names'])-3} more)"
        
        print(f"{sport:<20} {data['total_athletes']:<10} {data['qualified_athletes']:<10} {data['qualification_rate']:>6.1f}% {names_str}")
    
    print("-" * 80)
    print(f"{'TOTAL':<20} {total_athletes:<10} {total_qualified:<10} {total_qualified/total_athletes*100:>6.1f}%")
    
    # Team composition
    print(f"\n🇨🇭 SWISS OLYMPIC TEAM COMPOSITION (Milano Cortina 2026)")
    print("-" * 60)
    
    if total_qualified > 0:
        print(f"🏅 **{total_qualified} Swiss athletes have qualified for Milano Cortina 2026!**")
        print(f"📈 Overall qualification rate: {total_qualified/total_athletes*100:.1f}%")
        
        # Top performing sports
        top_sports = sorted(sport_summary.items(), key=lambda x: x[1]['qualification_rate'], reverse=True)
        print(f"\n🥇 Top performing sports by qualification rate:")
        for i, (sport, data) in enumerate(top_sports[:3], 1):
            if data['qualification_rate'] > 0:
                print(f"  {i}. {sport}: {data['qualification_rate']:.1f}% ({data['qualified_athletes']}/{data['total_athletes']})")
    else:
        print("❌ No athletes have qualified yet for Milano Cortina 2026")
        print("⚠️  Note: This may be due to limited data or upcoming qualification periods")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 60)
    
    for sport, data in sport_summary.items():
        if data['qualification_rate'] == 0 and data['total_athletes'] > 0:
            print(f"🎯 {sport}: Focus on upcoming World Cup/Championship events")
        elif 0 < data['qualification_rate'] < 50:
            print(f"📈 {sport}: Good progress, continue building on current results")
        elif data['qualification_rate'] >= 50:
            print(f"🏆 {sport}: Strong qualification performance, maintain current level")
    
    print(f"\n🏁 Analysis complete! Run 'python run_lookup.py' to explore individual athletes.")


if __name__ == "__main__":
    main()
