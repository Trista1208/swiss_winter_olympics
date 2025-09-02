import pandas as pd
from datetime import datetime

class BiathlonQualificationChecker:
    """
    Swiss Olympic Biathlon Team Selection - Qualification Checker
    
    Implements the 5 qualification routes defined in Biathlon_Hauptkriterien.txt
    """
    
    def __init__(self, results_df):
        self.df = results_df
        self.df_ranked = results_df[results_df['Rank_Clean'].notna() & (results_df['Rank_Clean'] > 0)]
        
        # Define the qualification routes
        self.routes = {
            1: "Top-3 in World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
            2: "1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26", 
            3: "1x Top-15 in World Cup 2025/26",
            4: "2x Top-25 in World Cup 2025/26",
            5: "1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"
        }
    
    def check_route_1(self, athlete_name):
        """Route 1: Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26"""
        
        athlete_results = self.df_ranked[self.df_ranked['Person'] == athlete_name]
        
        # Condition A: Top-3 at World Championships 2025
        wc_2025 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'IBU World Championships') & 
            (athlete_results['Year'] == 2025) & 
            (athlete_results['Rank_Clean'] <= 3)
        ]
        
        # Condition B: Top-30 in World Cup 2025/26
        wc_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 30)
        ]
        
        condition_a = len(wc_2025) >= 1
        condition_b = len(wc_2025_26) >= 1
        qualified = condition_a and condition_b
        
        return {
            'route': 1,
            'qualified': qualified,
            'condition_a': condition_a,
            'condition_b': condition_b,
            'details': {
                'wc_2025_top3': len(wc_2025),
                'wc_2025_26_top30': len(wc_2025_26),
                'wc_2025_results': wc_2025[['Date', 'Discipline', 'Rank_Clean']].to_dict('records'),
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records')
            }
        }
    
    def check_route_2(self, athlete_name):
        """Route 2: 1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26"""
        
        athlete_results = self.df_ranked[self.df_ranked['Person'] == athlete_name]
        
        # Condition A: Top-6 in World Cup 2024/25
        wc_2024_25 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2024-11-30') & 
            (athlete_results['Date'] <= '2025-03-23') &
            (athlete_results['Rank_Clean'] <= 6)
        ]
        
        # Condition B: Top-25 in World Cup 2025/26
        wc_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 25)
        ]
        
        condition_a = len(wc_2024_25) >= 1
        condition_b = len(wc_2025_26) >= 1
        qualified = condition_a and condition_b
        
        return {
            'route': 2,
            'qualified': qualified,
            'condition_a': condition_a,
            'condition_b': condition_b,
            'details': {
                'wc_2024_25_top6': len(wc_2024_25),
                'wc_2025_26_top25': len(wc_2025_26),
                'wc_2024_25_results': wc_2024_25[['Date', 'Discipline', 'Rank_Clean']].to_dict('records'),
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records')
            }
        }
    
    def check_route_3(self, athlete_name):
        """Route 3: 1x Top-15 in World Cup 2025/26"""
        
        athlete_results = self.df_ranked[self.df_ranked['Person'] == athlete_name]
        
        wc_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 15)
        ]
        
        qualified = len(wc_2025_26) >= 1
        
        return {
            'route': 3,
            'qualified': qualified,
            'details': {
                'wc_2025_26_top15': len(wc_2025_26),
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records')
            }
        }
    
    def check_route_4(self, athlete_name):
        """Route 4: 2x Top-25 in World Cup 2025/26"""
        
        athlete_results = self.df_ranked[self.df_ranked['Person'] == athlete_name]
        
        wc_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 25)
        ]
        
        qualified = len(wc_2025_26) >= 2
        
        return {
            'route': 4,
            'qualified': qualified,
            'details': {
                'wc_2025_26_top25': len(wc_2025_26),
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records')
            }
        }
    
    def check_route_5(self, athlete_name):
        """Route 5: 1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"""
        
        athlete_results = self.df_ranked[self.df_ranked['Person'] == athlete_name]
        
        # Condition A: Top-5 in IBU Cup 2025/26
        ibu_cup_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'IBU Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 5)
        ]
        
        # Condition B: 2x Top-30 in World Cup 2025/26
        wc_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 30)
        ]
        
        condition_a = len(ibu_cup_2025_26) >= 1
        condition_b = len(wc_2025_26) >= 2
        qualified = condition_a and condition_b
        
        return {
            'route': 5,
            'qualified': qualified,
            'condition_a': condition_a,
            'condition_b': condition_b,
            'details': {
                'ibu_cup_2025_26_top5': len(ibu_cup_2025_26),
                'wc_2025_26_top30': len(wc_2025_26),
                'ibu_cup_results': ibu_cup_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records'),
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records')
            }
        }
    
    def check_athlete_qualification(self, athlete_name):
        """Check all qualification routes for a specific athlete"""
        
        routes_results = {
            1: self.check_route_1(athlete_name),
            2: self.check_route_2(athlete_name), 
            3: self.check_route_3(athlete_name),
            4: self.check_route_4(athlete_name),
            5: self.check_route_5(athlete_name)
        }
        
        # Check if qualified through any route
        qualified = any(route['qualified'] for route in routes_results.values())
        qualified_routes = [route_num for route_num, result in routes_results.items() if result['qualified']]
        
        return {
            'athlete': athlete_name,
            'qualified': qualified,
            'qualified_routes': qualified_routes,
            'routes': routes_results
        }
    
    def generate_team_report(self):
        """Generate qualification status report for all Swiss athletes"""
        
        athletes = sorted(self.df['Person'].unique())
        report = {
            'summary': {
                'total_athletes': len(athletes),
                'qualified_athletes': 0,
                'men_qualified': 0,
                'women_qualified': 0
            },
            'athletes': {}
        }
        
        print("🇨🇭 SWISS OLYMPIC BIATHLON TEAM SELECTION REPORT")
        print("=" * 55)
        
        for athlete in athletes:
            result = self.check_athlete_qualification(athlete)
            report['athletes'][athlete] = result
            
            if result['qualified']:
                report['summary']['qualified_athletes'] += 1
                
                # Get gender
                gender = self.df[self.df['Person'] == athlete]['PersonGender'].iloc[0]
                if gender == 'Men':
                    report['summary']['men_qualified'] += 1
                else:
                    report['summary']['women_qualified'] += 1
        
        # Print summary
        print(f"📊 QUALIFICATION SUMMARY")
        print(f"Total Athletes: {report['summary']['total_athletes']}")
        print(f"Qualified Athletes: {report['summary']['qualified_athletes']}")
        print(f"  Men: {report['summary']['men_qualified']}")
        print(f"  Women: {report['summary']['women_qualified']}")
        
        print(f"\n🎯 QUALIFIED ATHLETES:")
        for athlete, result in report['athletes'].items():
            if result['qualified']:
                gender = self.df[self.df['Person'] == athlete]['PersonGender'].iloc[0]
                routes_str = ", ".join([f"Route {r}" for r in result['qualified_routes']])
                print(f"  ✅ {athlete} ({gender}) - {routes_str}")
        
        print(f"\n❌ NOT QUALIFIED:")
        for athlete, result in report['athletes'].items():
            if not result['qualified']:
                gender = self.df[self.df['Person'] == athlete]['PersonGender'].iloc[0]
                print(f"  ❌ {athlete} ({gender})")
        
        return report
    
    def detailed_athlete_report(self, athlete_name):
        """Generate detailed qualification report for a specific athlete"""
        
        result = self.check_athlete_qualification(athlete_name)
        
        print(f"\n🏔️ DETAILED QUALIFICATION REPORT: {athlete_name}")
        print("=" * 60)
        
        gender = self.df[self.df['Person'] == athlete_name]['PersonGender'].iloc[0]
        print(f"Gender: {gender}")
        print(f"Overall Status: {'✅ QUALIFIED' if result['qualified'] else '❌ NOT QUALIFIED'}")
        
        if result['qualified']:
            print(f"Qualified via: {', '.join([f'Route {r}' for r in result['qualified_routes']])}")
        
        print(f"\n📋 ROUTE-BY-ROUTE BREAKDOWN:")
        
        for route_num, route_result in result['routes'].items():
            route_desc = self.routes[route_num]
            status = "✅ QUALIFIED" if route_result['qualified'] else "❌ Not Qualified"
            
            print(f"\nRoute {route_num}: {status}")
            print(f"  Description: {route_desc}")
            
            # Show conditions for multi-condition routes
            if 'condition_a' in route_result:
                print(f"  Condition A: {'✅' if route_result['condition_a'] else '❌'}")
                print(f"  Condition B: {'✅' if route_result['condition_b'] else '❌'}")
            
            # Show relevant results
            details = route_result['details']
            for key, value in details.items():
                if isinstance(value, int) and value > 0:
                    print(f"  {key}: {value}")
                elif isinstance(value, list) and len(value) > 0:
                    print(f"  Recent results ({key}):")
                    for res in value[:3]:  # Show top 3 results
                        date = pd.to_datetime(res['Date']).strftime('%Y-%m-%d')
                        print(f"    {date}: Rank {int(res['Rank_Clean'])} in {res['Discipline']}")
        
        return result

def main():
    """Test the qualification system"""
    
    try:
        # Load the data
        df = pd.read_csv("cleaned_biathlon_results.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter for biathlon only
        df = df[df['Sport'] == 'Biathlon'].copy()
        
        print("🏔️ SWISS OLYMPIC BIATHLON QUALIFICATION SYSTEM")
        print("=" * 50)
        print(f"Analyzing {len(df)} biathlon results for {df['Person'].nunique()} athletes")
        
        # Create qualification checker
        checker = BiathlonQualificationChecker(df)
        
        # Generate team report
        team_report = checker.generate_team_report()
        
        # Show detailed report for top athletes
        print(f"\n" + "="*60)
        print("DETAILED REPORTS FOR TOP PERFORMERS")
        print("="*60)
        
        # Get athletes with best results
        top_athletes = ['Lena Häcki-Groß', 'Amy Baserga', 'Niklas Hartweg']
        
        for athlete in top_athletes:
            if athlete in df['Person'].values:
                checker.detailed_athlete_report(athlete)
        
        return checker, team_report
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    checker, report = main()
