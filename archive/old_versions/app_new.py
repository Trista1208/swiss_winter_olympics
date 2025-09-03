#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Team Selection Dashboard - Interactive Search & Filter Version
Search athletes by name, filter by sport and gender, view qualification status
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Import our analysis modules
from multi_sport_qualification_checker import MultiSportQualificationChecker

# Configure page
st.set_page_config(
    page_title="🏔️ Swiss Olympic Multi-Sport Dashboard",
    page_icon="🎿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, functional CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .athlete-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .athlete-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .athlete-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .athlete-details {
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    
    .qualification-status {
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    .qualified {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .not-qualified {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .no-results {
        text-align: center;
        color: #6c757d;
        font-style: italic;
        padding: 3rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_sports_data():
    """Load and return the complete dataset"""
    try:
        df = pd.read_csv('data/Results_Test_Version.csv')
        
        # Clean and process the data
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Clean rank column
        if 'Rank' in df.columns:
            df['Rank_Clean'] = df['Rank'].astype(str).str.extract(r'(\d+)')[0]
            df['Rank_Clean'] = pd.to_numeric(df['Rank_Clean'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data
def get_multi_sport_qualification_results(_checker, df):
    """Get qualification results for all sports"""
    try:
        results = {}
        sport_summaries = {}
        
        # Get all sports in the dataset
        all_sports = df['Sport'].unique() if 'Sport' in df.columns else []
        
        for sport in all_sports:
            sport_athletes = df[df['Sport'] == sport]
            if len(sport_athletes) > 0:
                qualified_count = 0
                sport_results = {}
                
                for athlete in sport_athletes['Name'].unique():
                    athlete_data = sport_athletes[sport_athletes['Name'] == athlete]
                    qual_result = _checker.check_athlete_qualification(athlete, sport.lower().replace(' ', '_'))
                    
                    is_qualified = any(route_info.get('qualified', False) for route_info in qual_result.values())
                    sport_results[athlete] = {
                        'qualified': is_qualified,
                        'routes': qual_result,
                        'data': athlete_data
                    }
                    
                    if is_qualified:
                        qualified_count += 1
                
                results[sport] = sport_results
                sport_summaries[sport] = {
                    'total_athletes': len(sport_athletes['Name'].unique()),
                    'qualified': qualified_count,
                    'qualification_rate': (qualified_count / len(sport_athletes['Name'].unique())) * 100
                }
        
        return results, sport_summaries
    except Exception as e:
        st.error(f"Error getting qualification results: {e}")
        return {}, {}

def create_athlete_card(athlete_name, athlete_info, sport):
    """Create a card display for an athlete"""
    is_qualified = athlete_info['qualified']
    athlete_data = athlete_info['data'].iloc[0] if len(athlete_info['data']) > 0 else {}
    
    # Get gender if available
    gender = athlete_data.get('Gender', 'N/A')
    
    # Count qualified routes
    qualified_routes = sum(1 for route_info in athlete_info['routes'].values() 
                          if route_info.get('qualified', False))
    
    status_class = "qualified" if is_qualified else "not-qualified"
    status_text = "✅ QUALIFIED" if is_qualified else "❌ Not Qualified"
    
    st.markdown(f"""
    <div class="athlete-card">
        <div class="athlete-name">{athlete_name}</div>
        <div class="athlete-details">
            <strong>Sport:</strong> {sport} | <strong>Gender:</strong> {gender}
        </div>
        <div class="athlete-details">
            <strong>Qualified Routes:</strong> {qualified_routes}/5
        </div>
        <span class="qualification-status {status_class}">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        🏔️ Swiss Olympic Multi-Sport Dashboard
        <br><small>Interactive Search & Filter System</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_all_sports_data()
    if df.empty:
        st.error("No data available")
        return
    
    # Initialize qualification checker
    checker = MultiSportQualificationChecker()
    
    # Get qualification results
    qualification_results, sport_summaries = get_multi_sport_qualification_results(checker, df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Search & Filter")
    
    # Search by athlete name
    search_name = st.sidebar.text_input("🔍 Search Athlete Name:", placeholder="Enter athlete name...")
    
    # Get all available sports and athletes
    all_sports = sorted(df['Sport'].unique()) if 'Sport' in df.columns else []
    all_athletes = sorted(df['Name'].unique()) if 'Name' in df.columns else []
    
    # Filter by sport
    selected_sports = st.sidebar.multiselect(
        "🏅 Filter by Sport:",
        options=["All"] + all_sports,
        default=["All"]
    )
    
    # Filter by gender
    genders = sorted(df['Gender'].unique()) if 'Gender' in df.columns else []
    selected_genders = st.sidebar.multiselect(
        "👤 Filter by Gender:",
        options=["All"] + list(genders),
        default=["All"]
    )
    
    # Filter by qualification status
    qualification_filter = st.sidebar.selectbox(
        "🎯 Qualification Status:",
        options=["All", "Qualified Only", "Not Qualified Only"]
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Overall statistics
        st.markdown("""
        <div class="stats-container">
            <h3>📊 Overall Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        total_athletes = len(df['Name'].unique()) if 'Name' in df.columns else 0
        total_qualified = sum(summary['qualified'] for summary in sport_summaries.values())
        
        st.metric("Total Athletes", total_athletes)
        st.metric("Qualified Athletes", total_qualified)
        st.metric("Qualification Rate", f"{(total_qualified/total_athletes*100):.1f}%" if total_athletes > 0 else "0%")
        
        # Sport breakdown
        st.markdown("### 🏅 Sport Breakdown")
        for sport, summary in sport_summaries.items():
            rate = summary['qualification_rate']
            st.metric(
                f"{sport}",
                f"{summary['qualified']}/{summary['total_athletes']}",
                f"{rate:.1f}%"
            )
    
    with col1:
        # Filter and display athletes
        filtered_athletes = []
        
        # Apply filters
        for sport, athletes in qualification_results.items():
            # Sport filter
            if "All" not in selected_sports and sport not in selected_sports:
                continue
                
            for athlete_name, athlete_info in athletes.items():
                # Name search filter
                if search_name and search_name.lower() not in athlete_name.lower():
                    continue
                
                # Gender filter
                athlete_data = athlete_info['data'].iloc[0] if len(athlete_info['data']) > 0 else {}
                athlete_gender = athlete_data.get('Gender', 'N/A')
                if "All" not in selected_genders and athlete_gender not in selected_genders:
                    continue
                
                # Qualification filter
                is_qualified = athlete_info['qualified']
                if qualification_filter == "Qualified Only" and not is_qualified:
                    continue
                elif qualification_filter == "Not Qualified Only" and is_qualified:
                    continue
                
                filtered_athletes.append((athlete_name, athlete_info, sport))
        
        # Display results
        if filtered_athletes:
            st.markdown(f"### 👥 Athletes ({len(filtered_athletes)} found)")
            
            # Sort athletes by name
            filtered_athletes.sort(key=lambda x: x[0])
            
            for athlete_name, athlete_info, sport in filtered_athletes:
                create_athlete_card(athlete_name, athlete_info, sport)
        else:
            st.markdown("""
            <div class="no-results">
                <h3>🔍 No athletes found</h3>
                <p>Try adjusting your search criteria or filters.</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
