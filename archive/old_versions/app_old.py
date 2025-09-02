#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Team Selection Dashboard
Interactive web interface for viewing athlete qualification status and performance across all sports
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .athlete-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .not-qualified-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .qualification-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .qualified {
        background-color: #d4edda;
        color: #155724;
    }
    .not-qualified {
        background-color: #f8d7da;
        color: #721c24;
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
        return {}

def create_athlete_overview_chart(df, qualification_results):
    """Create overview chart of qualified vs not qualified athletes"""
    qualified_count = 0
    not_qualified_count = 0
    
    for athlete, routes in qualification_results.items():
        if any(routes.values()):
            qualified_count += 1
        else:
            not_qualified_count += 1
    
    fig = go.Figure(data=[
        go.Bar(name='Qualified', x=['Men', 'Women'], y=[0, 0], marker_color='#28a745'),
        go.Bar(name='Not Qualified', x=['Men', 'Women'], y=[0, 0], marker_color='#dc3545')
    ])
    
    # Count by gender
    men_qualified = men_not_qualified = women_qualified = women_not_qualified = 0
    
    for athlete in qualification_results.keys():
        athlete_data = df[df['Person'] == athlete]
        if not athlete_data.empty:
            gender = athlete_data.iloc[0]['PersonGender']
            is_qualified = any(qualification_results[athlete].values())
            
            if gender == 'Men':
                if is_qualified:
                    men_qualified += 1
                else:
                    men_not_qualified += 1
            else:
                if is_qualified:
                    women_qualified += 1
                else:
                    women_not_qualified += 1
    
    fig = go.Figure(data=[
        go.Bar(name='Qualified', x=['Men', 'Women'], y=[men_qualified, women_qualified], marker_color='#28a745'),
        go.Bar(name='Not Qualified', x=['Men', 'Women'], y=[men_not_qualified, women_not_qualified], marker_color='#dc3545')
    ])
    
    fig.update_layout(
        title="Swiss Olympic Team Qualification Status",
        xaxis_title="Gender",
        yaxis_title="Number of Athletes",
        barmode='stack',
        height=400
    )
    
    return fig

def create_performance_chart(df, athlete_name):
    """Create performance trend chart for an athlete"""
    athlete_data = df[df['Person'] == athlete_name].copy()
    athlete_data = athlete_data.sort_values('Date')
    
    fig = px.line(
        athlete_data, 
        x='Date', 
        y='Rank_Clean',
        color='Discipline',
        title=f"Performance Trend - {athlete_name}",
        labels={'Rank_Clean': 'Rank', 'Date': 'Date'}
    )
    
    fig.update_layout(yaxis=dict(autorange="reversed"))  # Lower rank is better
    fig.update_layout(height=400)
    
    return fig

def display_athlete_card(athlete_name, df, qualification_results):
    """Display athlete information card"""
    athlete_data = df[df['Person'] == athlete_name]
    if athlete_data.empty:
        return
    
    athlete_info = athlete_data.iloc[0]
    routes = qualification_results.get(athlete_name, {})
    is_qualified = any(routes.values())
    qualified_routes = [route for route, status in routes.items() if status]
    
    card_class = "athlete-card" if is_qualified else "not-qualified-card"
    status_icon = "✅" if is_qualified else "❌"
    
    with st.container():
        st.markdown(f"""
        <div class="{card_class}">
            <h3>{status_icon} {athlete_name}</h3>
            <p><strong>Gender:</strong> {athlete_info['PersonGender']}</p>
            <p><strong>Age:</strong> {athlete_info['Age']} years</p>
            <p><strong>Total Races:</strong> {len(athlete_data)}</p>
            <p><strong>Best Rank:</strong> {athlete_data['Rank_Clean'].min()}</p>
            <p><strong>Status:</strong> {'QUALIFIED' if is_qualified else 'NOT QUALIFIED'}</p>
            {f"<p><strong>Qualified via:</strong> {', '.join(qualified_routes)}</p>" if qualified_routes else ""}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏔️ Swiss Olympic Multi-Sport Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### 2026 Milano Cortina Olympics Team Selection - All Sports")
    
    # Load data
    with st.spinner("Loading multi-sport data..."):
        df = load_all_sports_data()
    
    if df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Get qualification results
    with st.spinner("Analyzing qualification status across all sports..."):
        qualification_results, sport_summaries = get_multi_sport_qualification_results(df)
    
    # Sidebar navigation
    st.sidebar.title("🎿 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Overview", "👥 Athletes", "📈 Performance Analysis", "📋 Qualification Details"]
    )
    
    if page == "📊 Overview":
        st.header("Multi-Sport Team Selection Overview")
        
        # Key metrics across all sports
        total_athletes = len(df['Person'].unique())
        total_qualified = len(qualification_results)
        
        # Sport breakdown
        st.subheader("🏆 Sport-by-Sport Qualification Summary")
        
        # Create sport summary cards
        cols = st.columns(3)
        for i, (sport, summary) in enumerate(sport_summaries.items()):
            with cols[i % 3]:
                qualification_rate = (summary['qualified'] / summary['total'] * 100) if summary['total'] > 0 else 0
                
                st.markdown(f"""
                <div class="{'athlete-card' if summary['qualified'] > 0 else 'not-qualified-card'}">
                    <h4>🏅 {sport}</h4>
                    <p><strong>Qualified:</strong> {summary['qualified']}/{summary['total']}</p>
                    <p><strong>Rate:</strong> {qualification_rate:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Overall metrics
        st.subheader("📊 Overall Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{total_athletes}</h2>
                <p>Total Athletes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{total_qualified}</h2>
                <p>Qualified</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{total_athletes - total_qualified}</h2>
                <p>Not Qualified</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            qualification_rate = (total_qualified / total_athletes * 100) if total_athletes > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h2>{qualification_rate:.1f}%</h2>
                <p>Qualification Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Overview chart
        st.plotly_chart(create_athlete_overview_chart(df, qualification_results), use_container_width=True)
        
        # Quick stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Competition Statistics")
            st.write(f"**Total Races Analyzed:** {len(df)}")
            st.write(f"**Date Range:** {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
            st.write(f"**Competitions:** {df['Competition'].nunique()}")
            st.write(f"**Disciplines:** {df['Discipline'].nunique()}")
        
        with col2:
            st.subheader("🏆 Performance Highlights")
            podium_finishes = len(df[df['Rank_Clean'] <= 3])
            top10_finishes = len(df[df['Rank_Clean'] <= 10])
            st.write(f"**Podium Finishes (Top 3):** {podium_finishes}")
            st.write(f"**Top 10 Finishes:** {top10_finishes}")
            st.write(f"**Best Individual Rank:** {df['Rank_Clean'].min()}")
    
    elif page == "👥 Athletes":
        st.header("Athlete Profiles")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            gender_filter = st.selectbox("Filter by Gender:", ["All", "Men", "Women"])
        with col2:
            status_filter = st.selectbox("Filter by Status:", ["All", "Qualified", "Not Qualified"])
        
        # Filter athletes
        filtered_athletes = []
        for athlete_name in qualification_results.keys():
            athlete_data = df[df['Person'] == athlete_name]
            if athlete_data.empty:
                continue
                
            athlete_info = athlete_data.iloc[0]
            is_qualified = any(qualification_results[athlete_name].values())
            
            # Apply filters
            if gender_filter != "All" and athlete_info['PersonGender'] != gender_filter:
                continue
            if status_filter == "Qualified" and not is_qualified:
                continue
            if status_filter == "Not Qualified" and is_qualified:
                continue
                
            filtered_athletes.append(athlete_name)
        
        # Display athlete cards
        st.write(f"Showing {len(filtered_athletes)} athletes")
        
        for athlete_name in sorted(filtered_athletes):
            display_athlete_card(athlete_name, df, qualification_results)
    
    elif page == "📈 Performance Analysis":
        st.header("Performance Analysis")
        
        # Athlete selection
        selected_athlete = st.selectbox(
            "Select an athlete:",
            sorted(qualification_results.keys())
        )
        
        if selected_athlete:
            athlete_data = df[df['Person'] == selected_athlete]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📊 {selected_athlete} - Statistics")
                st.write(f"**Total Races:** {len(athlete_data)}")
                st.write(f"**Best Rank:** {athlete_data['Rank_Clean'].min()}")
                st.write(f"**Average Rank:** {athlete_data['Rank_Clean'].mean():.1f}")
                st.write(f"**Podium Finishes:** {len(athlete_data[athlete_data['Rank_Clean'] <= 3])}")
                st.write(f"**Top 10 Finishes:** {len(athlete_data[athlete_data['Rank_Clean'] <= 10])}")
            
            with col2:
                st.subheader("🎯 Qualification Status")
                routes = qualification_results[selected_athlete]
                for route, status in routes.items():
                    badge_class = "qualified" if status else "not-qualified"
                    status_text = "✅ QUALIFIED" if status else "❌ Not Qualified"
                    st.markdown(f"""
                    <div class="qualification-badge {badge_class}">
                        {route}: {status_text}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Performance chart
            st.plotly_chart(create_performance_chart(df, selected_athlete), use_container_width=True)
            
            # Recent results table
            st.subheader("📅 Recent Results")
            recent_results = athlete_data.sort_values('Date', ascending=False).head(10)
            display_cols = ['Date', 'Competition', 'Discipline', 'Rank_Clean', 'Season']
            st.dataframe(recent_results[display_cols])
    
    elif page == "📋 Qualification Details":
        st.header("Multi-Sport Qualification Route Details")
        
        # Sport selector
        selected_sport = st.selectbox(
            "Select Sport for Detailed Criteria:",
            sorted(df['Sport'].unique())
        )
        
        st.markdown(f"""
        ### 🎯 {selected_sport} Olympic Qualification Routes
        
        Swiss Olympic has defined 5 routes for {selected_sport.lower()} team qualification:
        """)
        
        # Show sport-specific qualification criteria
        if selected_sport == "Biathlon":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26
            2. **Route 2:** 1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26
            3. **Route 3:** 1x Top-15 in World Cup 2025/26
            4. **Route 4:** 2x Top-25 in World Cup 2025/26
            5. **Route 5:** 1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26
            """)
        elif selected_sport == "Alpine Skiing":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26
            2. **Route 2:** 1x Top-8 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26
            3. **Route 3:** 1x Top-10 in World Cup 2025/26
            4. **Route 4:** 2x Top-15 in World Cup 2025/26
            5. **Route 5:** 1x Top-5 in Europa Cup 2025/26 AND 2x Top-25 in World Cup 2025/26
            """)
        elif selected_sport == "Cross-Country Skiing":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26
            2. **Route 2:** 1x Top-10 in World Cup 2024/25 AND 1x Top-20 in World Cup 2025/26
            3. **Route 3:** 1x Top-15 in World Cup 2025/26
            4. **Route 4:** 2x Top-25 in World Cup 2025/26
            5. **Route 5:** 1x Top-5 in Continental Cup 2025/26 AND 2x Top-30 in World Cup 2025/26
            """)
        elif selected_sport == "Freestyle Skiing":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-20 in World Cup 2025/26
            2. **Route 2:** 1x Top-8 in World Cup 2024/25 AND 1x Top-16 in World Cup 2025/26
            3. **Route 3:** 1x Top-12 in World Cup 2025/26
            4. **Route 4:** 2x Top-20 in World Cup 2025/26
            5. **Route 5:** 1x Top-3 in Continental Cup 2025/26 AND 2x Top-25 in World Cup 2025/26
            """)
        elif selected_sport == "Bobsleigh":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-15 in World Cup 2025/26
            2. **Route 2:** 1x Top-8 in World Cup 2024/25 AND 1x Top-12 in World Cup 2025/26
            3. **Route 3:** 1x Top-10 in World Cup 2025/26
            4. **Route 4:** 2x Top-15 in World Cup 2025/26
            5. **Route 5:** 1x Top-3 in Europa Cup 2025/26 AND 2x Top-20 in World Cup 2025/26
            """)
        elif selected_sport == "Figure Skating":
            st.markdown("""
            1. **Route 1:** Top-3 at World Championships 2025 AND 1x Top-12 in Grand Prix 2025/26
            2. **Route 2:** 1x Top-6 in Grand Prix 2024/25 AND 1x Top-10 in Grand Prix 2025/26
            3. **Route 3:** 1x Top-8 in Grand Prix 2025/26 OR Top-5 in European Championships 2026
            4. **Route 4:** 2x Top-15 in International Competitions 2025/26
            5. **Route 5:** 1x Top-3 in Junior Grand Prix Final AND 1x Top-12 in Senior International
            """)
        else:
            st.info(f"Qualification criteria for {selected_sport} will be displayed here.")
        
        # Qualification summary table
        st.subheader("📊 Qualification Summary by Route")
        
        route_summary = {}
        for route_num in range(1, 6):
            route_key = f"Route {route_num}"
            qualified_count = sum(1 for routes in qualification_results.values() if routes.get(route_key, False))
            route_summary[route_key] = qualified_count
        
        summary_df = pd.DataFrame([
            {"Route": route, "Qualified Athletes": count}
            for route, count in route_summary.items()
        ])
        
        fig = px.bar(summary_df, x='Route', y='Qualified Athletes', 
                     title="Athletes Qualified by Route")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.subheader("📋 Detailed Athlete Breakdown")
        
        breakdown_data = []
        for athlete_name, routes in qualification_results.items():
            athlete_data = df[df['Person'] == athlete_name]
            if not athlete_data.empty:
                athlete_info = athlete_data.iloc[0]
                qualified_routes = [route for route, status in routes.items() if status]
                breakdown_data.append({
                    "Athlete": athlete_name,
                    "Gender": athlete_info['PersonGender'],
                    "Status": "✅ QUALIFIED" if qualified_routes else "❌ NOT QUALIFIED",
                    "Qualified Routes": ", ".join(qualified_routes) if qualified_routes else "None",
                    "Total Routes": len(qualified_routes)
                })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)

if __name__ == "__main__":
    main()
