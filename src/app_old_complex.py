#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Team Selection Dashboard - Interactive Search & Filter Version
Search athletes by name, filter by sport and gender, view qualification status
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import our analysis modules
from multi_sport_qualification_checker import MultiSportQualificationChecker

# Configure page
st.set_page_config(
    page_title="🏔️ Swiss Olympic Multi-Sport Dashboard",
    page_icon="🎿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, highly visible CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
        line-height: 1.1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        font-size: 1.8rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        opacity: 0.95;
    }
    
    .sport-category {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        margin: 2rem 0;
        border-left: 6px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .sport-category:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
    }
    
    .sport-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #2c3e50;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .sport-emoji {
        font-size: 2.5rem;
    }
    
    .sport-stats {
        display: flex;
        gap: 2rem;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #2c3e50;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .athletes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .athlete-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
        transition: all 0.3s ease;
    }
    
    .athlete-card.not-qualified {
        border-left-color: #dc3545;
    }
    
    .athlete-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    
    .athlete-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .athlete-status {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .qualified-status {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
    }
    
    .not-qualified-status {
        background: linear-gradient(45deg, #dc3545, #c82333);
        color: white;
    }
    
    .athlete-routes {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    .section-header {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 3rem 0 2rem 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .metric-card h2 {
        color: #2c3e50;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }
    
    .metric-card p {
        color: #6c757d;
        font-size: 1.1rem;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_sports_data():
    """Load and process all sports data"""
    try:
        # Load raw data
        df = pd.read_csv("data/Results_Test_Version.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        
        # Clean and process data
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        
        # Filter for Swiss athletes only
        df = df[df['Nationality'] == 'SUI'].copy()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_multi_sport_qualification_results(df):
    """Get qualification results for all athletes across all sports"""
    try:
        checker = MultiSportQualificationChecker(df)
        results = {}
        sport_summaries = {}
        
        # Get all sports
        sports = df['Sport'].unique()
        
        for sport in sports:
            sport_athletes = df[df['Sport'] == sport]['Person'].unique()
            qualified_athletes = []
            sport_athlete_details = {}
            
            for athlete in sport_athletes:
                if pd.notna(athlete):
                    athlete_qual = checker.check_athlete_qualification(athlete)
                    
                    if athlete_qual and not athlete_qual.get('error'):
                        sport_qual = athlete_qual['sports_qualifications'].get(sport, {})
                        is_qualified = sport_qual.get('qualified', False)
                        qualified_routes = sport_qual.get('qualified_routes', [])
                        
                        sport_athlete_details[athlete] = {
                            'qualified': is_qualified,
                            'routes': qualified_routes,
                            'sport': sport
                        }
                        
                        if is_qualified:
                            qualified_athletes.append(athlete)
                            results[athlete] = athlete_qual
            
            sport_summaries[sport] = {
                'total': len(sport_athletes),
                'qualified': len(qualified_athletes),
                'qualified_names': qualified_athletes,
                'all_athletes': sport_athlete_details
            }
        
        return results, sport_summaries
    except Exception as e:
        st.error(f"Error getting qualification results: {e}")
        return {}, {}

def get_sport_emoji(sport):
    """Get emoji for each sport"""
    sport_emojis = {
        'Biathlon': '🎯',
        'Alpine Skiing': '⛷️',
        'Cross-Country Skiing': '🎿',
        'Freestyle Skiing': '🤸',
        'Bobsleigh': '🛷',
        'Figure Skating': '⛸️'
    }
    return sport_emojis.get(sport, '🏔️')

def display_sport_category(sport, sport_data):
    """Display a complete sport category with all athletes"""
    emoji = get_sport_emoji(sport)
    qualification_rate = (sport_data['qualified'] / sport_data['total'] * 100) if sport_data['total'] > 0 else 0
    
    # Sport category container
    st.markdown(f"""
    <div class="sport-category">
        <div class="sport-title">
            <span class="sport-emoji">{emoji}</span>
            <span>{sport.upper()}</span>
        </div>
        
        <div class="sport-stats">
            <div class="stat-item">
                <span class="stat-number">{sport_data['total']}</span>
                <div class="stat-label">Total Athletes</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{sport_data['qualified']}</span>
                <div class="stat-label">Qualified</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">{qualification_rate:.1f}%</span>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Athletes grid
    athletes = sport_data['all_athletes']
    if athletes:
        # Sort athletes: qualified first, then alphabetically
        sorted_athletes = sorted(athletes.items(), key=lambda x: (not x[1]['qualified'], x[0]))
        
        # Create columns for athletes
        cols = st.columns(3)  # 3 athletes per row
        
        for i, (athlete_name, athlete_info) in enumerate(sorted_athletes):
            with cols[i % 3]:
                status_class = "qualified-status" if athlete_info['qualified'] else "not-qualified-status"
                card_class = "athlete-card" if athlete_info['qualified'] else "athlete-card not-qualified"
                status_text = "✅ QUALIFIED" if athlete_info['qualified'] else "❌ NOT QUALIFIED"
                status_icon = "✅" if athlete_info['qualified'] else "❌"
                
                routes_text = ""
                if athlete_info['qualified'] and athlete_info['routes']:
                    routes_text = f"<div class='athlete-routes'>Via: {', '.join(athlete_info['routes'])}</div>"
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="athlete-name">{status_icon} {athlete_name}</div>
                    <div class="athlete-status {status_class}">{status_text}</div>
                    {routes_text}
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main dashboard application with athlete names by sport categories"""
    
    # Header with animation
    st.markdown('<h1 class="main-header">🏔️ SWISS OLYMPIC TEAM</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Milano Cortina 2026 Winter Olympics - Athletes by Sport Categories</div>', unsafe_allow_html=True)
    
    # Load data with spinner
    with st.spinner("🔄 Loading Swiss Olympic data across all sports..."):
        df = load_all_sports_data()
    
    if df is None:
        st.error("❌ Failed to load data. Please check your data files.")
        return
    
    # Get qualification results
    with st.spinner("🎯 Analyzing qualification status across all sports..."):
        qualification_results, sport_summaries = get_multi_sport_qualification_results(df)
    
    # Sidebar navigation
    st.sidebar.markdown("## 🎿 Navigation")
    page = st.sidebar.selectbox(
        "Choose Dashboard Section:",
        ["🏆 Team Overview", "👥 Athletes by Sport", "📊 Sport Statistics", "📋 Qualification Routes"],
        index=1  # Default to Athletes by Sport
    )
    
    if page == "🏆 Team Overview":
        st.markdown('<h2 class="section-header">🏆 TEAM OVERVIEW</h2>', unsafe_allow_html=True)
        
        # Overall statistics
        total_athletes = len(df['Person'].unique())
        total_qualified = len(qualification_results)
        qualification_rate = (total_qualified / total_athletes * 100) if total_athletes > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>🇨🇭</h2>
                <h2>{total_athletes}</h2>
                <p>Total Athletes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2>✅</h2>
                <h2>{total_qualified}</h2>
                <p>Qualified</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2>⏳</h2>
                <h2>{total_athletes - total_qualified}</h2>
                <p>Pending</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h2>📈</h2>
                <h2>{qualification_rate:.1f}%</h2>
                <p>Success Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
    elif page == "👥 Athletes by Sport":
        st.markdown('<h2 class="section-header">👥 ATHLETES BY SPORT CATEGORIES</h2>', unsafe_allow_html=True)
        
        # Display each sport category with all athletes
        for sport in sorted(sport_summaries.keys()):
            display_sport_category(sport, sport_summaries[sport])
            st.markdown("---")  # Separator between sports
        
    elif page == "📊 Sport Statistics":
        st.markdown('<h2 class="section-header">📊 SPORT STATISTICS</h2>', unsafe_allow_html=True)
        
        # Prepare data for chart
        sport_data = []
        for sport, summary in sport_summaries.items():
            rate = (summary['qualified'] / summary['total'] * 100) if summary['total'] > 0 else 0
            sport_data.append({
                'Sport': sport,
                'Qualification Rate': rate,
                'Qualified': summary['qualified'],
                'Total': summary['total'],
                'Not Qualified': summary['total'] - summary['qualified']
            })
        
        chart_df = pd.DataFrame(sport_data)
        
        # Create qualification rate chart
        fig1 = px.bar(
            chart_df,
            x='Sport',
            y='Qualification Rate',
            color='Qualification Rate',
            color_continuous_scale='RdYlGn',
            title="Qualification Rates by Sport (%)",
            labels={'Qualification Rate': 'Qualification Rate (%)'}
        )
        
        fig1.update_layout(
            height=500,
            font=dict(size=14),
            title_font_size=20,
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Create stacked bar chart for qualified vs not qualified
        fig2 = px.bar(
            chart_df,
            x='Sport',
            y=['Qualified', 'Not Qualified'],
            title="Athletes by Qualification Status",
            color_discrete_map={'Qualified': '#28a745', 'Not Qualified': '#dc3545'}
        )
        
        fig2.update_layout(
            height=500,
            font=dict(size=14),
            title_font_size=20,
            xaxis_tickangle=-45,
            yaxis_title="Number of Athletes"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
    elif page == "📋 Qualification Routes":
        st.markdown('<h2 class="section-header">📋 QUALIFICATION ROUTES</h2>', unsafe_allow_html=True)
        
        # Sport selector
        selected_sport = st.selectbox(
            "Select Sport for Detailed Criteria:",
            sorted(df['Sport'].unique())
        )
        
        emoji = get_sport_emoji(selected_sport)
        st.markdown(f'<h3 style="color: white; text-align: center; font-size: 2rem;">{emoji} {selected_sport} Qualification Routes</h3>', unsafe_allow_html=True)
        
        # Show qualification criteria based on sport
        criteria_map = {
            "Biathlon": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
                "🥈 Route 2: 1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26",
                "🥉 Route 3: 1x Top-15 in World Cup 2025/26",
                "🏅 Route 4: 2x Top-25 in World Cup 2025/26",
                "🎯 Route 5: 1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"
            ],
            "Alpine Skiing": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
                "🥈 Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26",
                "🥉 Route 3: 1x Top-10 in World Cup 2025/26",
                "🏅 Route 4: 2x Top-15 in World Cup 2025/26",
                "🎯 Route 5: 1x Top-5 in Europa Cup 2025/26 AND 2x Top-25 in World Cup 2025/26"
            ],
            "Cross-Country Skiing": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
                "🥈 Route 2: 1x Top-10 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26",
                "🥉 Route 3: 1x Top-15 in World Cup 2025/26",
                "🏅 Route 4: 2x Top-25 in World Cup 2025/26",
                "🎯 Route 5: 1x Top-5 in Continental Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"
            ],
            "Freestyle Skiing": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-20 in World Cup 2025/26",
                "🥈 Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-16 in World Cup 2025/26",
                "🥉 Route 3: 1x Top-12 in World Cup 2025/26",
                "🏅 Route 4: 2x Top-20 in World Cup 2025/26",
                "🎯 Route 5: 1x Top-3 in Continental Cup 2025/26 AND 2x Top-25 in World Cup 2025/26"
            ],
            "Bobsleigh": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-15 in World Cup 2025/26",
                "🥈 Route 2: 1x Top-8 in World Cup 2024/25 AND 1x Top-12 in World Cup 2025/26",
                "🥉 Route 3: 1x Top-10 in World Cup 2025/26",
                "🏅 Route 4: 2x Top-15 in World Cup 2025/26",
                "🎯 Route 5: 1x Top-3 in Europa Cup 2025/26 AND 2x Top-20 in World Cup 2025/26"
            ],
            "Figure Skating": [
                "🥇 Route 1: Top-3 at World Championships 2025 AND 1x Top-12 in Grand Prix 2025/26",
                "🥈 Route 2: 1x Top-6 in Grand Prix 2024/25 AND 1x Top-10 in Grand Prix 2025/26",
                "🥉 Route 3: 1x Top-8 in Grand Prix 2025/26 OR Top-5 in European Championships 2026",
                "🏅 Route 4: 2x Top-15 in International Competitions 2025/26",
                "🎯 Route 5: 1x Top-3 in Junior Grand Prix Final AND 1x Top-12 in Senior International"
            ]
        }
        
        criteria = criteria_map.get(selected_sport, [])
        
        for criterion in criteria:
            st.markdown(f"""
            <div class="sport-category" style="margin: 1rem 0;">
                <h4 style="color: #2c3e50; font-size: 1.2rem; margin: 0;">{criterion}</h4>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
