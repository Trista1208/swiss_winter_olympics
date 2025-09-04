#!/usr/bin/env python3
"""
Multi-Sport Qualification Checker for Swiss Olympic Team Selection
Milano Cortina 2026 Olympics - CORRECTED QUALIFICATION SYSTEM

Updated based on Task Description PDF Section 3.1-3.6

Implements qualification criteria for:
- Biathlon (5 routes)
- Alpine Skiing (2 routes) 
- Cross-Country Skiing (6 routes)
- Figure Skating (score-based system)
- Bobsleigh (3 routes + team verification)
- Freestyle Skiing (Group A/B system)
"""

import pandas as pd
from datetime import datetime
import numpy as np

class MultiSportQualificationChecker:
    """
    Comprehensive qualification checker for all Swiss Olympic sports
    Milano Cortina 2026 Winter Olympics - CORRECTED VERSION
    """
    
    def __init__(self, results_df):
        self.df = results_df
        self.df_ranked = results_df[results_df['Rank_Clean'].notna() & (results_df['Rank_Clean'] > 0)]
        
        # Ensure required columns exist
        if 'Date' not in self.df.columns:
            self.df['Date'] = pd.to_datetime('2025-01-01')  # Default date
        if 'Year' not in self.df.columns:
            self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
            
    def check_qualification(self, athlete_name, sport):
        """Main qualification check dispatcher"""
        if sport == 'Biathlon':
            return self.check_biathlon_qualification(athlete_name)
        elif sport == 'Alpine Skiing':
            return self.check_alpine_skiing_qualification(athlete_name)
        elif sport == 'Cross-Country Skiing':
            return self.check_cross_country_qualification(athlete_name)
        elif sport == 'Figure Skating':
            return self.check_figure_skating_qualification(athlete_name)
        elif sport == 'Bobsleigh':
            return self.check_bobsleigh_qualification(athlete_name)
        elif sport == 'Freestyle Skiing':
            return self.check_freestyle_skiing_qualification(athlete_name)
        else:
            return {'qualified': False, 'reason': f'Unknown sport: {sport}'}

    # ========================================================================================
    # BIATHLON - 5 ROUTES (CORRECTED)
    # ========================================================================================
    
    def check_biathlon_qualification(self, athlete_name):
        """Check Biathlon qualification - 5 routes"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Biathlon') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No valid Biathlon results found'}
        
        routes = {}
        
        # Route 1: 1x Top-3 World Championships 2025 AND 1x Top-30 World Cup 2025/2026
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBU World Championships') &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top30 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'BMW IBU World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 30)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top30 >= 1)
        
        # Route 2: 1x Top-6 World Cup 2024/2025 AND 1x Top-25 World Cup 2025/2026
        wc_2024_25_top6 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'BMW IBU World Cup') &
            (athlete_data['Date'] >= '2024-11-30') & (athlete_data['Date'] <= '2025-03-23') &
            (athlete_data['Rank_Clean'] <= 6)
        ])
        
        wc_2025_26_top25 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'BMW IBU World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 25)
        ])
        
        routes['Route 2'] = (wc_2024_25_top6 >= 1) and (wc_2025_26_top25 >= 1)
        
        # Route 3: 1x Top-15 World Cup 2025/2026
        wc_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'BMW IBU World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 3'] = wc_2025_26_top15 >= 1
        
        # Route 4: 2x Top-25 World Cup 2025/2026
        routes['Route 4'] = wc_2025_26_top25 >= 2
        
        # Route 5: 1x Top-5 IBU Cup 2025/2026 AND 2x Top-30 World Cup 2025/2026
        ibu_cup_top5 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBU Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 5)
        ])
        
        routes['Route 5'] = (ibu_cup_top5 >= 1) and (wc_2025_26_top30 >= 2)
        
        qualified = any(routes.values())
        
        return {
            'qualified': qualified,
            'sport': 'Biathlon',
            'routes': routes,
            'qualifying_routes': [k for k, v in routes.items() if v]
        }

    # ========================================================================================
    # ALPINE SKIING - 2 ROUTES (CORRECTED)
    # ========================================================================================
    
    def check_alpine_skiing_qualification(self, athlete_name):
        """Check Alpine Skiing qualification - 2 routes (SIMPLIFIED)"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Alpine Skiing') &
            (self.df_ranked['Class'] == 'Seniors') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No valid Alpine Skiing results found'}
        
        routes = {}
        
        # Route 1: 1x Top-7 World Cup 2025/2026
        wc_2025_26_top7 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'Audi FIS Ski World Cup') &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-01-25') &
            (athlete_data['Rank_Clean'] <= 7)
        ])
        
        routes['Route 1'] = wc_2025_26_top7 >= 1
        
        # Route 2: 2x Top-15 World Cup 2025/2026
        wc_2025_26_top15 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'Audi FIS Ski World Cup') &
            (athlete_data['Date'] >= '2025-10-01') & (athlete_data['Date'] <= '2026-01-25') &
            (athlete_data['Rank_Clean'] <= 15)
        ])
        
        routes['Route 2'] = wc_2025_26_top15 >= 2
        
        qualified = any(routes.values())
        
        return {
            'qualified': qualified,
            'sport': 'Alpine Skiing',
            'routes': routes,
            'qualifying_routes': [k for k, v in routes.items() if v]
        }

    # ========================================================================================
    # CROSS-COUNTRY SKIING - 6 ROUTES (CORRECTED)
    # ========================================================================================
    
    def check_cross_country_qualification(self, athlete_name):
        """Check Cross-Country Skiing qualification - 6 routes"""
        
        # Base filter (Seniors for most competitions)
        athlete_data_seniors = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Cross-Country Skiing') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        # Special filter for U23 World Championships (allows Under 23)
        athlete_data_u23 = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Cross-Country Skiing') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Under 23')
        ]
        
        if athlete_data_seniors.empty and athlete_data_u23.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No valid Cross-Country Skiing results found'}
        
        routes = {}
        
        # Route 1: 1x Top-3 World Championships 2025 AND 1x Top-30 World Cup 2025/2026
        wc_2025_top3 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Nordic World Ski Championships') &
            (athlete_data_seniors['Year'] == 2025) &
            (athlete_data_seniors['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top30 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Cross-Country World Cup') &
            (athlete_data_seniors['Date'] >= '2025-08-01') & (athlete_data_seniors['Date'] <= '2026-01-21') &
            (athlete_data_seniors['Rank_Clean'] <= 30)
        ])
        
        routes['Route 1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top30 >= 1)
        
        # Route 2: 1x Top-3 U23 World Championships 2025 AND 1x Top-25 World Cup 2025/2026
        u23_wc_2025_top3 = len(athlete_data_u23[
            (athlete_data_u23['Comp.SetDetail'] == 'FIS Nordic Under 23 World Ski Championships') &
            (athlete_data_u23['Year'] == 2025) &
            (athlete_data_u23['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top25 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Cross-Country World Cup') &
            (athlete_data_seniors['Date'] >= '2025-08-01') & (athlete_data_seniors['Date'] <= '2026-01-21') &
            (athlete_data_seniors['Rank_Clean'] <= 25)
        ])
        
        routes['Route 2'] = (u23_wc_2025_top3 >= 1) and (wc_2025_26_top25 >= 1)
        
        # Route 3: 1x Top-3 World Cup 2024/2025 AND 1x Top-25 World Cup 2025/2026
        wc_2024_25_top3 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Cross-Country World Cup') &
            (athlete_data_seniors['Date'] >= '2024-11-29') & (athlete_data_seniors['Date'] <= '2025-07-31') &
            (athlete_data_seniors['Rank_Clean'] <= 3)
        ])
        
        routes['Route 3'] = (wc_2024_25_top3 >= 1) and (wc_2025_26_top25 >= 1)
        
        # Route 4: 1x Top-15 World Cup 2025/2026
        wc_2025_26_top15 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Cross-Country World Cup') &
            (athlete_data_seniors['Date'] >= '2025-08-01') & (athlete_data_seniors['Date'] <= '2026-01-21') &
            (athlete_data_seniors['Rank_Clean'] <= 15)
        ])
        
        routes['Route 4'] = wc_2025_26_top15 >= 1
        
        # Route 5: 2x Top-25 World Cup 2025/2026
        routes['Route 5'] = wc_2025_26_top25 >= 2
        
        # Route 6: 1x Top-3 Continental Cup 2025/2026 AND (1x Top-25 WC 2024/25 OR 1x Top-25 WC 2025/26)
        cc_2025_26_top3 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FESA Cross-Country Continental Cup') &
            (athlete_data_seniors['Date'] >= '2025-08-01') & (athlete_data_seniors['Date'] <= '2026-01-21') &
            (athlete_data_seniors['Rank_Clean'] <= 3)
        ])
        
        wc_2024_25_top25 = len(athlete_data_seniors[
            (athlete_data_seniors['Comp.SetDetail'] == 'FIS Cross-Country World Cup') &
            (athlete_data_seniors['Date'] >= '2024-11-29') & (athlete_data_seniors['Date'] <= '2025-07-31') &
            (athlete_data_seniors['Rank_Clean'] <= 25)
        ])
        
        routes['Route 6'] = (cc_2025_26_top3 >= 1) and ((wc_2024_25_top25 >= 1) or (wc_2025_26_top25 >= 1))
        
        qualified = any(routes.values())
        
        return {
            'qualified': qualified,
            'sport': 'Cross-Country Skiing',
            'routes': routes,
            'qualifying_routes': [k for k, v in routes.items() if v]
        }

    # ========================================================================================
    # FIGURE SKATING - SCORE-BASED SYSTEM (CORRECTED)
    # ========================================================================================
    
    def check_figure_skating_qualification(self, athlete_name):
        """Check Figure Skating qualification - Score-based system"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Figure Skating') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'reason': 'No valid Figure Skating results found'}
        
        # Score thresholds by discipline and gender
        thresholds = {
            ('Singles', 'Women'): 185,
            ('Singles', 'Men'): 210,
            ('Ice Dance', 'Mixed'): 165,
            ('Pairs', 'Mixed'): 170
        }
        
        # Eligible competitions
        eligible_comps = [
            'ISU World Figure Skating Championships',
            'ISU European Figure Skating Championships',
            'ISU Grand Prix Senior',
            'ISU Challenger Senior',
            'ISU Olympic Qualifier',
            'ISU OWG Test Event',
            'National Championships'
        ]
        
        qualification_results = {}
        
        for discipline in athlete_data['Discipline'].unique():
            for gender in athlete_data[athlete_data['Discipline'] == discipline]['Gender'].unique():
                key = (discipline, gender)
                if key in thresholds:
                    threshold = thresholds[key]
                    
                    # Find best result in eligible competitions
                    best_results = athlete_data[
                        (athlete_data['Discipline'] == discipline) &
                        (athlete_data['Gender'] == gender) &
                        (athlete_data['Comp.SetDetail'].isin(eligible_comps)) &
                        (athlete_data['Result'].notna())
                    ]
                    
                    if not best_results.empty:
                        best_score = best_results['Result'].max()
                        qualified = best_score >= threshold
                        
                        qualification_results[f"{discipline}_{gender}"] = {
                            'qualified': qualified,
                            'best_score': best_score,
                            'threshold': threshold,
                            'discipline': discipline,
                            'gender': gender
                        }
        
        overall_qualified = any(result['qualified'] for result in qualification_results.values())
        
        return {
            'qualified': overall_qualified,
            'sport': 'Figure Skating',
            'qualification_system': 'score_based',
            'results': qualification_results,
            'qualifying_disciplines': [k for k, v in qualification_results.items() if v['qualified']]
        }

    # ========================================================================================
    # BOBSLEIGH - 3 ROUTES + TEAM VERIFICATION (CORRECTED)
    # ========================================================================================
    
    def check_bobsleigh_qualification(self, athlete_name):
        """Check Bobsleigh qualification - 3 routes with team verification"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Bobsleigh') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'routes': {}, 'reason': 'No valid Bobsleigh results found'}
        
        routes = {}
        
        # Route 1: 1x Top-6 World Cup 2025/2026 AND (Top-6 WC 2025 OR Top-6 WC Lillehammer 2024/25)
        wc_2025_26_top6 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBSF World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 6)
        ])
        
        wc_2025_top6 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBSF World Championships') &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 6)
        ])
        
        wc_lillehammer_top6 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBSF World Cup') &
            (athlete_data['Date'] >= '2025-02-03') & (athlete_data['Date'] <= '2025-02-09') &
            (athlete_data['Host City'] == 'Lillehammer') &
            (athlete_data['Rank_Clean'] <= 6)
        ])
        
        routes['Route 1'] = (wc_2025_26_top6 >= 1) and ((wc_2025_top6 >= 1) or (wc_lillehammer_top6 >= 1))
        
        # Route 2: 2x Top-12 World Cup 2025/2026 (requires commitment until 2030)
        wc_2025_26_top12 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBSF World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 12)
        ])
        
        routes['Route 2'] = wc_2025_26_top12 >= 2
        routes['Route 2 Note'] = 'REQUIRES_COMMITMENT_2030'
        
        # Route 3: 2x Top-14 World Cup 2025/2026 AND Age <= 27
        wc_2025_26_top14 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'IBSF World Cup') &
            (athlete_data['Date'] >= '2025-11-01') & (athlete_data['Date'] <= '2026-01-18') &
            (athlete_data['Rank_Clean'] <= 14)
        ])
        
        # Check age (if available)
        age_condition = True  # Default to True if age not available
        if 'Age' in athlete_data.columns:
            age_condition = athlete_data['Age'].min() <= 27
        
        routes['Route 3'] = (wc_2025_26_top14 >= 2) and age_condition
        
        # TODO: Implement team verification for 2-Man and 4-Man disciplines
        # This requires matching individual results with team results
        
        qualified = any(v for k, v in routes.items() if not k.endswith('Note'))
        
        return {
            'qualified': qualified,
            'sport': 'Bobsleigh',
            'routes': routes,
            'qualifying_routes': [k for k, v in routes.items() if v and not k.endswith('Note')],
            'team_verification': 'TODO: Implement for 2-Man/4-Man disciplines'
        }

    # ========================================================================================
    # FREESTYLE SKIING - GROUP A/B SYSTEM (CORRECTED)
    # ========================================================================================
    
    def check_freestyle_skiing_qualification(self, athlete_name):
        """Check Freestyle Skiing qualification - Group A/B system"""
        
        athlete_data = self.df_ranked[
            (self.df_ranked['Person'] == athlete_name) & 
            (self.df_ranked['Sport'] == 'Freestyle Skiing') &
            (self.df_ranked['Is Olympic Discipline'] == 'Yes') &
            (self.df_ranked['Team Members'] == 'No') &
            (self.df_ranked['Class'] == 'Seniors')
        ]
        
        if athlete_data.empty:
            return {'qualified': False, 'reason': 'No valid Freestyle Skiing results found'}
        
        group_a_routes = {}
        group_b_routes = {}
        
        # GROUP A ROUTES (same for all disciplines)
        
        # Route A1: 1x Top-3 World Championships 2025 AND 1x Top-8 World Cup 2025/26
        wc_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'FIS Freestyle World Ski Championships') &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        wc_2025_26_top8 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'FIS Freeski World Cup') &
            (athlete_data['Date'] >= '2025-07-01') & (athlete_data['Date'] <= '2026-01-25') &
            (athlete_data['Rank_Clean'] <= 8)
        ])
        
        group_a_routes['Route A1'] = (wc_2025_top3 >= 1) and (wc_2025_26_top8 >= 1)
        
        # Route A2: 1x Top-3 World Cup Standings 2024/2025 AND 1x Top-8 World Cup 2025/26
        wc_standings_2025_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'FIS Freeski World Cup Standings') &
            (athlete_data['Year'] == 2025) &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        group_a_routes['Route A2'] = (wc_standings_2025_top3 >= 1) and (wc_2025_26_top8 >= 1)
        
        # Route A3: 2x Top-3 World Cup 2025/2026
        wc_2025_26_top3 = len(athlete_data[
            (athlete_data['Comp.SetDetail'] == 'FIS Freeski World Cup') &
            (athlete_data['Date'] >= '2025-07-01') & (athlete_data['Date'] <= '2026-01-25') &
            (athlete_data['Rank_Clean'] <= 3)
        ])
        
        group_a_routes['Route A3'] = wc_2025_26_top3 >= 2
        
        # GROUP B ROUTES
        
        # Route B1: 1x Top-8 World Cup 2025/2026 (common for all disciplines)
        group_b_routes['Route B1'] = wc_2025_26_top8 >= 1
        
        # Routes B2 & B3: Discipline-specific (simplified implementation)
        # TODO: Implement full discipline-specific logic
        group_b_routes['Route B2/B3'] = 'TODO: Implement discipline-specific routes'
        
        group_a_qualified = any(group_a_routes.values())
        group_b_qualified = any(v for v in group_b_routes.values() if isinstance(v, bool))
        
        return {
            'qualified': group_a_qualified or group_b_qualified,
            'sport': 'Freestyle Skiing',
            'group_a': {
                'qualified': group_a_qualified,
                'routes': group_a_routes,
                'priority': 1
            },
            'group_b': {
                'qualified': group_b_qualified,
                'routes': group_b_routes,
                'priority': 2
            },
            'final_group': 'A' if group_a_qualified else ('B' if group_b_qualified else 'None')
        }

    # ========================================================================================
    # UTILITY METHODS
    # ========================================================================================
    
    def get_all_qualifications(self, athlete_name):
        """Get qualification status for all sports for a given athlete"""
        sports = ['Biathlon', 'Alpine Skiing', 'Cross-Country Skiing', 
                 'Figure Skating', 'Bobsleigh', 'Freestyle Skiing']
        
        results = {}
        for sport in sports:
            try:
                results[sport] = self.check_qualification(athlete_name, sport)
            except Exception as e:
                results[sport] = {'qualified': False, 'error': str(e)}
        
        return results
    
    def get_qualified_athletes_by_sport(self, sport):
        """Get all qualified athletes for a specific sport"""
        athletes = self.df[self.df['Sport'] == sport]['Person'].unique()
        qualified = []
        
        for athlete in athletes:
            result = self.check_qualification(athlete, sport)
            if result.get('qualified', False):
                qualified.append({
                    'athlete': athlete,
                    'sport': sport,
                    'qualification': result
                })
        
        return qualified
    
    def check_athlete_qualification(self, athlete_name):
        """Check qualification for an athlete across all sports (legacy method for compatibility)"""
        try:
            # Get all sports this athlete participates in
            athlete_sports = self.df[self.df['Person'] == athlete_name]['Sport'].unique()
            
            sports_qualifications = {}
            overall_qualified = False
            
            for sport in athlete_sports:
                try:
                    sport_result = self.check_qualification(athlete_name, sport)
                    sports_qualifications[sport] = sport_result
                    
                    if sport_result.get('qualified', False):
                        overall_qualified = True
                        
                except Exception as e:
                    sports_qualifications[sport] = {
                        'qualified': False,
                        'error': str(e)
                    }
            
            return {
                'athlete': athlete_name,
                'qualified': overall_qualified,
                'sports_qualifications': sports_qualifications
            }
            
        except Exception as e:
            return {
                'athlete': athlete_name,
                'qualified': False,
                'error': str(e)
            }