#!/usr/bin/env python3
"""
Biathlon Qualification Checker for Swiss Olympic Team Selection
Milano Cortina 2026 Olympics - CORRECTED VERSION

Updated based on Task Description PDF Section 3.1

Implements the 5 qualification routes defined in Biathlon_Hauptkriterien.txt
"""

import pandas as pd
from datetime import datetime

class BiathlonQualificationChecker:
    """
    Swiss Olympic Biathlon Team Selection - Qualification Checker
    CORRECTED VERSION - Based on Task Description PDF
    
    Implements the 5 qualification routes:
    1. 1x Top-3 World Championships 2025 AND 1x Top-30 World Cup 2025/2026
    2. 1x Top-6 World Cup 2024/2025 AND 1x Top-25 World Cup 2025/2026  
    3. 1x Top-15 World Cup 2025/2026
    4. 2x Top-25 World Cup 2025/2026
    5. 1x Top-5 IBU Cup 2025/2026 AND 2x Top-30 World Cup 2025/2026
    """
    
    def __init__(self, results_df):
        self.df = results_df
        self.df_ranked = results_df[results_df['Rank_Clean'].notna() & (results_df['Rank_Clean'] > 0)]
        
        # Define the CORRECTED qualification routes
        self.routes = {
            1: "1x Top-3 World Championships 2025 AND 1x Top-30 World Cup 2025/2026",
            2: "1x Top-6 World Cup 2024/2025 AND 1x Top-25 World Cup 2025/2026", 
            3: "1x Top-15 World Cup 2025/2026",
            4: "2x Top-25 World Cup 2025/2026",
            5: "1x Top-5 IBU Cup 2025/2026 AND 2x Top-30 World Cup 2025/2026"
        }
    
    def check_route_1(self, athlete_name):
        """Route 1: 1x Top-3 World Championships 2025 AND 1x Top-30 World Cup 2025/2026"""
        
        athlete_results = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Condition A: Top-3 at World Championships 2025
        wc_2025 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'IBU World Championships') & 
            (athlete_results['Year'] == 2025) &
            (athlete_results['Rank_Clean'] <= 3)
        ]
        
        # Condition B: Top-30 in World Cup 2025/2026
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
                'wc_2025_results': wc_2025[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025.empty else [],
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025_26.empty else []
            }
        }
    
    def check_route_2(self, athlete_name):
        """Route 2: 1x Top-6 World Cup 2024/2025 AND 1x Top-25 World Cup 2025/2026"""
        
        athlete_results = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Condition A: Top-6 in World Cup 2024/2025
        wc_2024_25 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'BMW IBU World Cup') & 
            (athlete_results['Date'] >= '2024-11-30') & 
            (athlete_results['Date'] <= '2025-03-23') &
            (athlete_results['Rank_Clean'] <= 6)
        ]
        
        # Condition B: Top-25 in World Cup 2025/2026
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
                'wc_2024_25_results': wc_2024_25[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2024_25.empty else [],
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025_26.empty else []
            }
        }
    
    def check_route_3(self, athlete_name):
        """Route 3: 1x Top-15 World Cup 2025/2026"""
        
        athlete_results = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Condition: Top-15 in World Cup 2025/2026
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
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025_26.empty else []
            }
        }
    
    def check_route_4(self, athlete_name):
        """Route 4: 2x Top-25 World Cup 2025/2026"""
        
        athlete_results = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Condition: 2x Top-25 in World Cup 2025/2026
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
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025_26.empty else []
            }
        }
    
    def check_route_5(self, athlete_name):
        """Route 5: 1x Top-5 IBU Cup 2025/2026 AND 2x Top-30 World Cup 2025/2026"""
        
        athlete_results = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Condition A: Top-5 in IBU Cup 2025/2026
        ibu_cup_2025_26 = athlete_results[
            (athlete_results['Comp.SetDetail'] == 'IBU Cup') & 
            (athlete_results['Date'] >= '2025-11-01') & 
            (athlete_results['Date'] <= '2026-01-18') &
            (athlete_results['Rank_Clean'] <= 5)
        ]
        
        # Condition B: 2x Top-30 in World Cup 2025/2026
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
                'ibu_cup_results': ibu_cup_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not ibu_cup_2025_26.empty else [],
                'wc_2025_26_results': wc_2025_26[['Date', 'Discipline', 'Rank_Clean']].to_dict('records') if not wc_2025_26.empty else []
            }
        }
    
    def check_qualification(self, athlete_name):
        """Check all qualification routes for an athlete"""
        
        results = {}
        routes_qualified = []
        
        # Check all 5 routes
        for route_num in range(1, 6):
            route_method = getattr(self, f'check_route_{route_num}')
            route_result = route_method(athlete_name)
            results[f'route_{route_num}'] = route_result
            
            if route_result['qualified']:
                routes_qualified.append(route_num)
        
        # Overall qualification status
        overall_qualified = len(routes_qualified) > 0
        
        return {
            'athlete': athlete_name,
            'sport': 'Biathlon',
            'qualified': overall_qualified,
            'qualifying_routes': routes_qualified,
            'route_details': results,
            'routes_description': self.routes
        }
    
    def get_all_qualified_athletes(self):
        """Get all qualified Biathlon athletes"""
        
        athletes = self.df['Person'].unique()
        qualified_athletes = []
        
        for athlete in athletes:
            result = self.check_qualification(athlete)
            if result['qualified']:
                qualified_athletes.append(result)
        
        return qualified_athletes
    
    def generate_summary_report(self):
        """Generate a summary report of all athletes and their qualification status"""
        
        athletes = self.df['Person'].unique()
        report = {
            'total_athletes': len(athletes),
            'qualified_athletes': 0,
            'athletes_by_route': {i: [] for i in range(1, 6)},
            'detailed_results': []
        }
        
        for athlete in athletes:
            result = self.check_qualification(athlete)
            report['detailed_results'].append(result)
            
            if result['qualified']:
                report['qualified_athletes'] += 1
                for route in result['qualifying_routes']:
                    report['athletes_by_route'][route].append(athlete)
        
        return report