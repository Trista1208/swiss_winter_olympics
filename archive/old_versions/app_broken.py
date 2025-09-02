#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Team Selection Dashboard - REDESIGNED UI
Interactive web interface with enhanced visibility and modern design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# Import our analysis modules
from biathlon_analysis import main as load_data
from qualification_checker import BiathlonQualificationChecker
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
    
    .sport-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        margin: 1.5rem 0;
        border: 3px solid transparent;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .sport-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 60px rgba(0,0,0,0.2);
    }
    
    .sport-card.qualified {
        border: 3px solid #28a745;
        background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%);
        box-shadow: 0 15px 40px rgba(40, 167, 69, 0.3);
    }
    
    .sport-card.not-qualified {
        border: 3px solid #dc3545;
        background: linear-gradient(145deg, #f8d7da 0%, #f1b0b7 100%);
        box-shadow: 0 15px 40px rgba(220, 53, 69, 0.3);
    }
    
    .sport-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
    }
    
    .sport-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        color: #2c3e50;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sport-emoji {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
        display: block;
    }
    
    .sport-stats {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 2px solid #e9ecef;
    }
    
    .stat-container {
        text-align: center;
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 900;
        color: #2c3e50;
        display: block;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        text-align: center;
        border: none;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 30px 70px rgba(0,0,0,0.2);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
    }
    
    .metric-card h2 {
        color: #2c3e50;
        font-size: 4rem;
        margin-bottom: 1rem;
        font-weight: 900;
        line-height: 1;
    }
    
    .metric-card p {
        color: #6c757d;
        font-size: 1.4rem;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
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
    
    .qualification-badge {
        display: inline-block;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .qualified-badge {
        background: linear-gradient(45deg, #28a745, #20c997, #17a2b8);
        color: white;
        border: none;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .qualified-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(40, 167, 69, 0.4);
    }
    
    .not-qualified-badge {
        background: linear-gradient(45deg, #dc3545, #c82333, #bd2130);
        color: white;
        border: none;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .not-qualified-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(220, 53, 69, 0.4);
    }
    
    .athlete-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 6px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .athlete-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        border-left-color: #764ba2;
    }
    
    .progress-container {
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .progress-bar {
        height: 25px;
        border-radius: 15px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        margin: 1rem 0;
        overflow: hidden;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);
        position: relative;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        border: 2px solid #e9ecef;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_sports_data():
    """Load and process all sports data"""
    try:
        # Load raw data
        df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
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
            
            for athlete in sport_athletes:
                if pd.notna(athlete):
                    athlete_qual = checker.check_athlete_qualification(athlete)
                    
                    if athlete_qual and not athlete_qual.get('error'):
                        sport_qual = athlete_qual['sports_qualifications'].get(sport, {})
                        if sport_qual.get('qualified', False):
                            qualified_athletes.append(athlete)
                            results[athlete] = athlete_qual
            
            sport_summaries[sport] = {
                'total': len(sport_athletes),
                'qualified': len(qualified_athletes),
                'qualified_names': qualified_athletes
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

def create_sport_card(sport, summary):
    """Create a visually striking sport card"""
    qualification_rate = (summary['qualified'] / summary['total'] * 100) if summary['total'] > 0 else 0
    card_class = "qualified" if summary['qualified'] > 0 else "not-qualified"
    emoji = get_sport_emoji(sport)
    
    return f"""
    <div class="sport-card {card_class}">
        <div class="sport-emoji">{emoji}</div>
        <div class="sport-title">{sport}</div>
        <div class="sport-stats">
            <div class="stat-container">
                <span class="stat-number">{summary['qualified']}</span>
                <div class="stat-label">Qualified</div>
            </div>
            <div class="stat-container">
                <span class="stat-number">{summary['total']}</span>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat-container">
                <span class="stat-number">{qualification_rate:.1f}%</span>
                <div class="stat-label">Rate</div>
            </div>
        </div>
    </div>
    """

def main():
    """Main dashboard application with enhanced UI"""
    
    # Header with animation
    st.markdown('<h1 class="main-header">🏔️ SWISS OLYMPIC TEAM</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Milano Cortina 2026 Winter Olympics - Multi-Sport Qualification Dashboard</div>', unsafe_allow_html=True)
    
    # Load data with spinner
    with st.spinner("🔄 Loading Swiss Olympic data across all sports..."):
        df = load_all_sports_data()
    
    if df is None:
        st.error("❌ Failed to load data. Please check your data files.")
        return
    
    # Get qualification results
    with st.spinner("🎯 Analyzing qualification status across all sports..."):
        qualification_results, sport_summaries = get_multi_sport_qualification_results(df)
    
    # Sidebar navigation with enhanced styling
    st.sidebar.markdown("## 🎿 Navigation")
    page = st.sidebar.selectbox(
        "Choose Dashboard Section:",
        ["🏆 Team Overview", "📊 Sport Analysis", "👥 Athlete Profiles", "📋 Qualification Routes"],
        index=0
    )
    
    if page == "🏆 Team Overview":
        st.markdown('<h2 class="section-header">🏆 TEAM OVERVIEW</h2>', unsafe_allow_html=True)
        
        # Overall statistics with enhanced metrics
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
        
        # Progress bar
        st.markdown('<h2 class="section-header">🎯 OVERALL PROGRESS</h2>', unsafe_allow_html=True)
        progress_html = f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {qualification_rate}%;"></div>
            <div style="text-align: center; color: white; font-weight: bold; font-size: 1.2rem; margin-top: 1rem;">
                {total_qualified} of {total_athletes} athletes qualified ({qualification_rate:.1f}%)
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        
    elif page == "📊 Sport Analysis":
        st.markdown('<h2 class="section-header">📊 SPORT-BY-SPORT ANALYSIS</h2>', unsafe_allow_html=True)
        
        # Create sport cards in a responsive grid
        cols = st.columns(2)
        for i, (sport, summary) in enumerate(sport_summaries.items()):
            with cols[i % 2]:
                st.markdown(create_sport_card(sport, summary), unsafe_allow_html=True)
        
        # Sport comparison chart
        st.markdown('<h2 class="section-header">📈 QUALIFICATION COMPARISON</h2>', unsafe_allow_html=True)
        
        # Prepare data for chart
        sport_data = []
        for sport, summary in sport_summaries.items():
            rate = (summary['qualified'] / summary['total'] * 100) if summary['total'] > 0 else 0
            sport_data.append({
                'Sport': sport,
                'Qualification Rate': rate,
                'Qualified': summary['qualified'],
                'Total': summary['total']
            })
        
        chart_df = pd.DataFrame(sport_data)
        
        # Create bar chart
        fig = px.bar(
            chart_df,
            x='Sport',
            y='Qualification Rate',
            color='Qualification Rate',
            color_continuous_scale='Viridis',
            title="Qualification Rates by Sport",
            labels={'Qualification Rate': 'Qualification Rate (%)'}
        )
        
        fig.update_layout(
            height=500,
            font=dict(size=14),
            title_font_size=20,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif page == "👥 Athlete Profiles":
        st.markdown('<h2 class="section-header">👥 ATHLETE PROFILES</h2>', unsafe_allow_html=True)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_sport = st.selectbox("Filter by Sport:", ["All Sports"] + sorted(df['Sport'].unique()))
        with col2:
            status_filter = st.selectbox("Filter by Status:", ["All", "Qualified", "Not Qualified"])
        
        # Filter data
        display_df = df.copy()
        if selected_sport != "All Sports":
            display_df = display_df[display_df['Sport'] == selected_sport]
        
        athletes = display_df['Person'].unique()
        
        # Display athletes
        for athlete in sorted(athletes)[:20]:  # Show first 20
            if pd.notna(athlete):
                athlete_sports = display_df[display_df['Person'] == athlete]['Sport'].unique()
                
                # Check qualification status
                is_qualified = athlete in qualification_results
                if status_filter == "Qualified" and not is_qualified:
                    continue
                elif status_filter == "Not Qualified" and is_qualified:
                    continue
                
                badge_class = "qualified-badge" if is_qualified else "not-qualified-badge"
                status_text = "QUALIFIED" if is_qualified else "NOT QUALIFIED"
                
                athlete_html = f"""
                <div class="athlete-card">
                    <h3>🏃‍♂️ {athlete}</h3>
                    <p><strong>Sports:</strong> {', '.join(athlete_sports)}</p>
                    <div class="qualification-badge {badge_class}">{status_text}</div>
                </div>
                """
                st.markdown(athlete_html, unsafe_allow_html=True)
        
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
        
        for i, criterion in enumerate(criteria, 1):
            route_html = f"""
            <div class="athlete-card" style="margin: 1rem 0;">
                <h4 style="color: #2c3e50; font-size: 1.3rem;">{criterion}</h4>
            </div>
            """
            st.markdown(route_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
