#!/usr/bin/env python3
"""
Multi-Sport Qualification Checker for Swiss Olympic Team Selection
Milano Cortina 2026 Olympics - All Sports Qualification System

Implements qualification criteria for:
- Biathlon
- Alpine Skiing  
- Cross-Country Skiing
- Freestyle Skiing
- Bobsleigh
- Figure Skating
"""

import pandas as pd
from datetime import datetime
from qualification_checker import BiathlonQualificationChecker

class MultiSportQualificationChecker:
    """
    Comprehensive qualification checker for all Swiss Olympic sports
    Milano Cortina 2026 Winter Olympics
    """
    
    def __init__(self, results_df):
        self.df = results_df
        self.df_ranked = results_df[results_df['Rank_Clean'].notna() & (results_df['Rank_Clean'] > 0)]
        
        # Initialize sport-specific checkers
        self.biathlon_checker = BiathlonQualificationChecker(
            results_df[results_df['Sport'] == 'Biathlon']
        ) if not results_df[results_df['Sport'] == 'Biathlon'].empty else None
        
    def check_alpine_skiing_qualification(self, athlete_name):
        """Check Alpine Skiing qualification (5 routes)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Alpine Skiing')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No Alpine Skiing results found'}
        
        routes = {}
        
        # Route 1: Top-3 in World Championships 2025 AND 1x Top-30 in World Cup 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Championships', na=False)) &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top30 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 30)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top30 >= 1)
        
        # Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26
        wc_2024_25_top8 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2024-10-01') & (athlete_data['Date'] <= '2025-03-31') &
            (athlete_data['Rank_Clean'] <= 8)
        ])
        
        wc_2025_26_top20 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 20)
        ])
        
        routes['Route 2'] = (wc_2024_25_top8 >= 1) and (wc_2025_26_top20 >= 1)
        
        # Route 3: 1x Top-10 in World Cup 2025/26
        wc_2025_26_top10 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 10)
        ])
        
        routes['Route 3'] = wc_2025_26_top10 >= 1
        
        # Route 4: 2x Top-15 in World Cup 2025/26
        wc_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 4'] = wc_2025_26_top15 >= 2
        
        # Route 5: 1x Top-5 in Europa Cup 2025/26 AND 2x Top-25 in World Cup 2025/26
        europa_cup_top5 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Europa Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 5)
        ])
        
        wc_2025_26_top25 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 25)
        ])
        
        routes['Route 5'] = (europa_cup_top5 >= 1) and (wc_2025_26_top25 >= 2)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes,
            'sport': 'Alpine Skiing'
        }
    
    def check_cross_country_qualification(self, athlete_name):
        """Check Cross-Country Skiing qualification (5 routes)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Cross-Country Skiing')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No Cross-Country Skiing results found'}
        
        routes = {}
        
        # Route 1: Top-3 in World Championships 2025 AND 1x Top-30 in World Cup 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Championships', na=False)) &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top30 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 30)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top30 >= 1)
        
        # Route 2: 1x Top-10 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26
        wc_2024_25_top10 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2024-11-01') & (athlete_data['Date'] <= '2025-03-31') &
            (athlete_data['Rank_Clean'] <= 10)
        ])
        
        wc_2025_26_top20 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 20)
        ])
        
        routes['Route 2'] = (wc_2024_25_top10 >= 1) and (wc_2025_26_top20 >= 1)
        
        # Route 3: 1x Top-15 in World Cup 2025/26
        wc_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 3'] = wc_2025_26_top15 >= 1
        
        # Route 4: 2x Top-25 in World Cup 2025/26
        wc_2025_26_top25 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 25)
        ])
        
        routes['Route 4'] = wc_2025_26_top25 >= 2
        
        # Route 5: 1x Top-5 in Continental Cup 2025/26 AND 2x Top-30 in World Cup 2025/26
        continental_cup_top5 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Continental Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 5)
        ])
        
        wc_2025_26_top30_route5 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 30)
        ])
        
        routes['Route 5'] = (continental_cup_top5 >= 1) and (wc_2025_26_top30_route5 >= 2)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes,
            'sport': 'Cross-Country Skiing'
        }
    
    def check_freestyle_skiing_qualification(self, athlete_name):
        """Check Freestyle Skiing qualification (5 routes)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Freestyle Skiing')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No Freestyle Skiing results found'}
        
        routes = {}
        
        # Route 1: Top-3 in World Championships 2025 AND 1x Top-20 in World Cup 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Championships', na=False)) &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top20 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 20)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top20 >= 1)
        
        # Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-16 in World Cup 2025/26
        wc_2024_25_top8 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2024-10-01') & (athlete_data['Date'] <= '2025-04-30') &
            (athlete_data['Rank_Clean'] <= 8)
        ])
        
        wc_2025_26_top16 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 16)
        ])
        
        routes['Route 2'] = (wc_2024_25_top8 >= 1) and (wc_2025_26_top16 >= 1)
        
        # Route 3: 1x Top-12 in World Cup 2025/26
        wc_2025_26_top12 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 12)
        ])
        
        routes['Route 3'] = wc_2025_26_top12 >= 1
        
        # Route 4: 2x Top-20 in World Cup 2025/26
        wc_2025_26_top20_route4 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 20)
        ])
        
        routes['Route 4'] = wc_2025_26_top20_route4 >= 2
        
        # Route 5: 1x Top-3 in Continental Cup 2025/26 AND 2x Top-25 in World Cup 2025/26
        continental_cup_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Continental Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top25 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-03-31') &
            (athlete_data['Rank_Clean'] <= 25)
        ])
        
        routes['Route 5'] = (continental_cup_top3 >= 1) and (wc_2025_26_top25 >= 2)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes,
            'sport': 'Freestyle Skiing'
        }
    
    def check_bobsleigh_qualification(self, athlete_name):
        """Check Bobsleigh qualification (5 routes)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Bobsleigh')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No Bobsleigh results found'}
        
        routes = {}
        
        # Route 1: Top-3 in World Championships 2025 AND 1x Top-15 in World Cup 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Championships', na=False)) &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top15 >= 1)
        
        # Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-12 in World Cup 2025/26
        wc_2024_25_top8 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2024-11-01') & (athlete_data['Date'] <= '2025-03-15') &
            (athlete_data['Rank_Clean'] <= 8)
        ])
        
        wc_2025_26_top12 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 12)
        ])
        
        routes['Route 2'] = (wc_2024_25_top8 >= 1) and (wc_2025_26_top12 >= 1)
        
        # Route 3: 1x Top-10 in World Cup 2025/26
        wc_2025_26_top10 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 10)
        ])
        
        routes['Route 3'] = wc_2025_26_top10 >= 1
        
        # Route 4: 2x Top-15 in World Cup 2025/26
        wc_2025_26_top15_route4 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 4'] = wc_2025_26_top15_route4 >= 2
        
        # Route 5: 1x Top-3 in Europa Cup 2025/26 AND 2x Top-20 in World Cup 2025/26
        europa_cup_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Europa Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top20 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Cup', na=False)) &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-02-15') &
            (athlete_data['Rank_Clean'] <= 20)
        ])
        
        routes['Route 5'] = (europa_cup_top3 >= 1) and (wc_2025_26_top20 >= 2)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes,
            'sport': 'Bobsleigh'
        }
    
    def check_figure_skating_qualification(self, athlete_name):
        """Check Figure Skating qualification (5 routes)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Figure Skating')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No Figure Skating results found'}
        
        routes = {}
        
        # Route 1: Top-3 in World Championships 2025 AND 1x Top-12 in Grand Prix 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('World Championships', na=False)) &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        gp_2025_26_top12 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2025-12-15') &
            (athlete_data['Rank_Clean'] <= 12)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (gp_2025_26_top12 >= 1)
        
        # Route 2: 1x Top-6 in Grand Prix 2024/25 AND 1x Top-10 in Grand Prix 2025/26
        gp_2024_25_top6 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix', na=False)) &
            (athlete_data['Date'] >= '2024-10-01') & (athlete_data['Date'] <= '2024-12-15') &
            (athlete_data['Rank_Clean'] <= 6)
        ])
        
        gp_2025_26_top10 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2025-12-15') &
            (athlete_data['Rank_Clean'] <= 10)
        ])
        
        routes['Route 2'] = (gp_2024_25_top6 >= 1) and (gp_2025_26_top10 >= 1)
        
        # Route 3: 1x Top-8 in Grand Prix 2025/26 OR Top-5 in European Championships 2026
        gp_2025_26_top8 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix', na=False)) &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2025-12-15') &
            (athlete_data['Rank_Clean'] <= 8)
        ])
        
        euro_2026_top5 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('European Championships', na=False)) &
            (athlete_data['Year'] == 2026) &
            (athlete_data['Rank_Clean'] <= 5)
        ])
        
        routes['Route 3'] = (gp_2025_26_top8 >= 1) or (euro_2026_top5 >= 1)
        
        # Route 4: 2x Top-15 in International Competitions 2025/26
        international_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix|Challenger|Championships', na=False)) &
            (athlete_data['Date'] >= '2025-07-01') & (athlete_data['Date'] <= '2026-01-31') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 4'] = international_2025_26_top15 >= 2
        
        # Route 5: 1x Top-3 in Junior Grand Prix Final AND 1x Top-12 in Senior International
        jgp_final_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Junior Grand Prix Final', na=False)) &
            (athlete_data['Date'] >= '2024-07-01') & (athlete_data['Date'] <= '2025-12-31') &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        senior_international_top12 = len(athlete_data[
            (athlete_data['Comp.SetDetail'].str.contains('Grand Prix|Challenger', na=False)) &
            (athlete_data['Date'] >= '2025-07-01') & (athlete_data['Date'] <= '2026-01-31') &
            (athlete_data['Rank_Clean'] <= 12)
        ])
        
        routes['Route 5'] = (jgp_final_top3 >= 1) and (senior_international_top12 >= 1)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes,
            'sport': 'Figure Skating'
        }
    
    def check_athlete_qualification(self, athlete_name):
        """Check qualification for an athlete across all their sports"""
        
        athlete_data = self.df[self.df['Person'] == athlete_name]
        if athlete_data.empty:
            return {'error': 'Athlete not found'}
        
        sports = athlete_data['Sport'].unique()
        qualifications = {}
        
        for sport in sports:
            if sport == 'Biathlon' and self.biathlon_checker:
                # Use existing biathlon checker
                biathlon_result = {}
                for route in range(1, 6):
                    method_name = f"check_route_{route}"
                    if hasattr(self.biathlon_checker, method_name):
                        route_result = getattr(self.biathlon_checker, method_name)(athlete_name)
                        if isinstance(route_result, dict) and 'qualified' in route_result:
                            biathlon_result[f"Route {route}"] = route_result['qualified']
                        else:
                            biathlon_result[f"Route {route}"] = bool(route_result)
                
                is_qualified = any(biathlon_result.values())
                qualified_routes = [route for route, status in biathlon_result.items() if status]
                
                qualifications['Biathlon'] = {
                    'qualified': is_qualified,
                    'routes': biathlon_result,
                    'qualified_routes': qualified_routes,
                    'sport': 'Biathlon'
                }
                
            elif sport == 'Alpine Skiing':
                qualifications['Alpine Skiing'] = self.check_alpine_skiing_qualification(athlete_name)
            elif sport == 'Cross-Country Skiing':
                qualifications['Cross-Country Skiing'] = self.check_cross_country_qualification(athlete_name)
            elif sport == 'Freestyle Skiing':
                qualifications['Freestyle Skiing'] = self.check_freestyle_skiing_qualification(athlete_name)
            elif sport == 'Bobsleigh':
                qualifications['Bobsleigh'] = self.check_bobsleigh_qualification(athlete_name)
            elif sport == 'Figure Skating':
                qualifications['Figure Skating'] = self.check_figure_skating_qualification(athlete_name)
        
        # Determine overall qualification status
        overall_qualified = any(
            qual.get('qualified', False) for qual in qualifications.values()
            if isinstance(qual, dict)
        )
        
        qualified_sports = [
            sport for sport, qual in qualifications.items()
            if isinstance(qual, dict) and qual.get('qualified', False)
        ]
        
        return {
            'athlete': athlete_name,
            'overall_qualified': overall_qualified,
            'qualified_sports': qualified_sports,
            'sports_qualifications': qualifications,
            'total_sports': len(sports)
        }


def main():
    """Test the multi-sport qualification system"""
    
    print("🏔️ MULTI-SPORT QUALIFICATION CHECKER - MILANO CORTINA 2026")
    print("=" * 65)
    
    # Load data
    try:
        df = pd.read_csv("data/Results_Test_Version.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        df = df[df['Nationality'] == 'SUI'].copy()  # Swiss athletes only
        
        print(f"✅ Data loaded: {len(df)} Swiss results across {len(df['Sport'].unique())} sports")
        
        # Initialize checker
        checker = MultiSportQualificationChecker(df)
        
        # Test with sample athletes from different sports
        test_athletes = [
            'Amy Baserga',  # Biathlon
            'Marco Odermatt',  # Alpine (if exists)
            'Dario Cologna',  # Cross-Country (if exists)
        ]
        
        # Get actual athletes from each sport
        for sport in df['Sport'].unique():
            sport_athletes = df[df['Sport'] == sport]['Person'].unique()
            if len(sport_athletes) > 0:
                test_athletes.append(sport_athletes[0])  # Add first athlete from each sport
        
        test_athletes = list(set(test_athletes))  # Remove duplicates
        
        print(f"\n🎯 TESTING QUALIFICATION FOR {len(test_athletes)} ATHLETES:")
        print("-" * 55)
        
        qualified_count = 0
        for athlete in test_athletes[:10]:  # Test first 10
            if pd.notna(athlete):
                result = checker.check_athlete_qualification(athlete)
                
                if 'error' in result:
                    print(f"❌ {athlete}: {result['error']}")
                    continue
                
                status = "✅ QUALIFIED" if result['overall_qualified'] else "❌ NOT QUALIFIED"
                sports = ", ".join(result['qualified_sports']) if result['qualified_sports'] else "None"
                
                print(f"{status[:2]} {athlete:<25} | {sports}")
                
                if result['overall_qualified']:
                    qualified_count += 1
        
        print(f"\n📊 SUMMARY:")
        print(f"Qualified Athletes: {qualified_count}")
        print(f"Total Tested: {min(10, len(test_athletes))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
