#!/usr/bin/env python3
"""
Swiss Olympic Athlete Lookup System
Interactive tool to search for athletes, filter by sport, and check qualification status
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import our analysis modules
from biathlon_analysis import main as load_data
from qualification_checker import BiathlonQualificationChecker

# Configure page
st.set_page_config(
    page_title="🔍 Swiss Olympic Athlete Lookup",
    page_icon="🎿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .search-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
    }
    .athlete-result {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .not-qualified-result {
        border-left: 5px solid #dc3545;
    }
    .no-qualification-result {
        border-left: 5px solid #6c757d;
    }
    .qualification-status {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
    }
    .qualified-badge {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .not-qualified-badge {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .no-data-badge {
        background-color: #e2e3e5;
        color: #383d41;
        border: 1px solid #d6d8db;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .info-item {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .info-label {
        font-weight: bold;
        color: #495057;
        font-size: 0.9rem;
    }
    .info-value {
        font-size: 1.2rem;
        color: #212529;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    """Load all sports data, not just biathlon"""
    try:
        # Load the original CSV with all sports
        df = pd.read_csv("Results_Test_Version.csv", sep=';', encoding='utf-8')
        
        # Clean column names
        df.columns = df.columns.str.strip('"')
        
        # Convert date columns
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
        df['DoB'] = pd.to_datetime(df['DoB'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        
        # Clean rank column
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract('(\d+)')[0], errors='coerce')
        
        # Add season column
        df['Season'] = df['Date'].apply(lambda x: f"{x.year-1}/{x.year}" if x.month <= 6 else f"{x.year}/{x.year+1}")
        
        # Filter for Swiss athletes only
        df = df[df['Nationality'] == 'SUI'].copy()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_biathlon_qualification_status(athlete_name, df):
    """Get biathlon qualification status for an athlete"""
    try:
        # Filter for biathlon only
        biathlon_df = df[df['Sport'] == 'Biathlon'].copy()
        
        if biathlon_df.empty:
            return None, "No biathlon data available"
        
        athlete_data = biathlon_df[biathlon_df['Person'] == athlete_name]
        if athlete_data.empty:
            return None, "Athlete not found in biathlon results"
        
        checker = BiathlonQualificationChecker(biathlon_df)
        
        routes = {}
        for route in range(1, 6):
            method_name = f"check_route_{route}"
            if hasattr(checker, method_name):
                routes[f"Route {route}"] = getattr(checker, method_name)(athlete_name)
        
        is_qualified = any(routes.values())
        qualified_routes = [route for route, status in routes.items() if status]
        
        return {
            'is_qualified': is_qualified,
            'routes': routes,
            'qualified_routes': qualified_routes
        }, None
        
    except Exception as e:
        return None, f"Error checking qualification: {e}"

def display_athlete_info(athlete_name, df):
    """Display comprehensive athlete information"""
    
    # Get all data for this athlete
    athlete_data = df[df['Person'] == athlete_name]
    
    if athlete_data.empty:
        st.error(f"No data found for athlete: {athlete_name}")
        return
    
    # Get basic info
    athlete_info = athlete_data.iloc[0]
    sports = athlete_data['Sport'].unique()
    
    # Determine qualification status
    qualification_info = None
    qualification_error = None
    
    if 'Biathlon' in sports:
        qualification_info, qualification_error = get_biathlon_qualification_status(athlete_name, df)
    
    # Determine result container class
    if qualification_info and qualification_info['is_qualified']:
        container_class = "athlete-result"
        status_badge_class = "qualified-badge"
        status_text = "✅ QUALIFIED FOR 2026 OLYMPICS"
    elif qualification_info and not qualification_info['is_qualified']:
        container_class = "athlete-result not-qualified-result"
        status_badge_class = "not-qualified-badge"
        status_text = "❌ NOT QUALIFIED FOR 2026 OLYMPICS"
    else:
        container_class = "athlete-result no-qualification-result"
        status_badge_class = "no-data-badge"
        status_text = "ℹ️ NO BIATHLON QUALIFICATION DATA"
    
    # Display athlete card
    with st.container():
        st.markdown(f"""
        <div class="{container_class}">
            <h2>🏃‍♂️ {athlete_name}</h2>
            <div class="qualification-status {status_badge_class}">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Basic information grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">Gender</div>
                <div class="info-value">{athlete_info['PersonGender']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            age = athlete_info['Age'] if pd.notna(athlete_info['Age']) else "N/A"
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">Age</div>
                <div class="info-value">{age}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">Sports</div>
                <div class="info-value">{len(sports)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-label">Total Results</div>
                <div class="info-value">{len(athlete_data)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sports breakdown
        st.subheader("🏆 Sports & Performance")
        
        sports_summary = []
        for sport in sports:
            sport_data = athlete_data[athlete_data['Sport'] == sport]
            best_rank = sport_data['Rank_Clean'].min()
            total_races = len(sport_data)
            podiums = len(sport_data[sport_data['Rank_Clean'] <= 3])
            
            sports_summary.append({
                'Sport': sport,
                'Total Races': total_races,
                'Best Rank': best_rank if pd.notna(best_rank) else "N/A",
                'Podium Finishes': podiums,
                'Recent Competition': sport_data['Date'].max().strftime('%Y-%m-%d') if pd.notna(sport_data['Date'].max()) else "N/A"
            })
        
        sports_df = pd.DataFrame(sports_summary)
        st.dataframe(sports_df, use_container_width=True)
        
        # Qualification details (if biathlon)
        if qualification_info:
            st.subheader("🎯 Olympic Qualification Details")
            
            if qualification_info['is_qualified']:
                st.success(f"✅ **QUALIFIED** via: {', '.join(qualification_info['qualified_routes'])}")
            else:
                st.error("❌ **NOT QUALIFIED** for 2026 Olympics")
            
            # Route breakdown
            st.write("**Route-by-Route Breakdown:**")
            route_descriptions = {
                "Route 1": "Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
                "Route 2": "1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26",
                "Route 3": "1x Top-15 in World Cup 2025/26",
                "Route 4": "2x Top-25 in World Cup 2025/26",
                "Route 5": "1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"
            }
            
            for route, status in qualification_info['routes'].items():
                status_icon = "✅" if status else "❌"
                description = route_descriptions.get(route, "Unknown route")
                st.write(f"{status_icon} **{route}**: {description}")
        
        elif qualification_error:
            st.info(f"ℹ️ Qualification Status: {qualification_error}")
        
        # Recent results
        st.subheader("📅 Recent Results")
        recent_results = athlete_data.sort_values('Date', ascending=False).head(10)
        display_cols = ['Date', 'Sport', 'Competition', 'Discipline', 'Rank_Clean', 'Season']
        available_cols = [col for col in display_cols if col in recent_results.columns]
        st.dataframe(recent_results[available_cols], use_container_width=True)

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Swiss Olympic Athlete Lookup</h1>', unsafe_allow_html=True)
    st.markdown("### Search for athletes, filter by sport, and check Olympic qualification status")
    
    # Load data
    with st.spinner("Loading Swiss Olympic athlete data..."):
        df = load_all_data()
    
    if df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Search interface
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        st.subheader("🔍 Search & Filter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Athlete name search
            all_athletes = sorted(df['Person'].dropna().unique())
            
            search_option = st.radio(
                "Search Method:",
                ["Type athlete name", "Select from dropdown"],
                horizontal=True
            )
            
            if search_option == "Type athlete name":
                athlete_name = st.text_input(
                    "Enter athlete name:",
                    placeholder="e.g., Amy Baserga, Niklas Hartweg...",
                    help="Start typing an athlete's name"
                )
                
                # Auto-suggest matching names
                if athlete_name:
                    matching_athletes = [name for name in all_athletes if athlete_name.lower() in name.lower()]
                    if matching_athletes and athlete_name not in matching_athletes:
                        st.write("**Suggestions:**")
                        for match in matching_athletes[:5]:
                            if st.button(f"🎯 {match}", key=f"suggest_{match}"):
                                athlete_name = match
                                st.rerun()
            else:
                athlete_name = st.selectbox(
                    "Select athlete:",
                    [""] + all_athletes,
                    help="Choose an athlete from the dropdown"
                )
        
        with col2:
            # Sport filter
            all_sports = sorted(df['Sport'].unique())
            selected_sport = st.selectbox(
                "Filter by sport (optional):",
                ["All Sports"] + all_sports,
                help="Filter results by specific sport"
            )
            
            # Gender filter
            gender_filter = st.selectbox(
                "Filter by gender (optional):",
                ["All", "Men", "Women"]
            )
            
            # Show statistics
            filtered_df = df.copy()
            if selected_sport != "All Sports":
                filtered_df = filtered_df[filtered_df['Sport'] == selected_sport]
            if gender_filter != "All":
                filtered_df = filtered_df[filtered_df['PersonGender'] == gender_filter]
            
            st.info(f"📊 **Current filters:** {len(filtered_df['Person'].unique())} athletes, {len(filtered_df)} results")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Search results
    if athlete_name and athlete_name.strip():
        # Check if athlete exists
        if athlete_name in all_athletes:
            display_athlete_info(athlete_name, df)
        else:
            st.error(f"❌ Athlete '{athlete_name}' not found in the database.")
            
            # Show similar names
            similar_names = [name for name in all_athletes if athlete_name.lower() in name.lower()]
            if similar_names:
                st.write("**Did you mean:**")
                for name in similar_names[:10]:
                    if st.button(f"🔍 {name}", key=f"similar_{name}"):
                        st.session_state.athlete_name = name
                        st.rerun()
    
    else:
        # Show browse options
        st.subheader("📋 Browse Athletes")
        
        # Filter athletes based on current filters
        browse_df = df.copy()
        if selected_sport != "All Sports":
            browse_df = browse_df[browse_df['Sport'] == selected_sport]
        if gender_filter != "All":
            browse_df = browse_df[browse_df['PersonGender'] == gender_filter]
        
        athletes_to_show = sorted(browse_df['Person'].unique())
        
        if athletes_to_show:
            st.write(f"**{len(athletes_to_show)} athletes match your filters:**")
            
            # Show athletes in columns
            cols = st.columns(3)
            for i, athlete in enumerate(athletes_to_show):
                with cols[i % 3]:
                    if st.button(f"🔍 {athlete}", key=f"browse_{athlete}"):
                        st.session_state.selected_athlete = athlete
                        st.rerun()
        else:
            st.warning("No athletes found matching your filters.")
        
        # Quick stats
        st.subheader("📊 Database Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Athletes", len(df['Person'].unique()))
        with col2:
            st.metric("Sports Covered", len(df['Sport'].unique()))
        with col3:
            biathlon_athletes = len(df[df['Sport'] == 'Biathlon']['Person'].unique())
            st.metric("Biathlon Athletes", biathlon_athletes)
        with col4:
            st.metric("Total Results", len(df))

if __name__ == "__main__":
    main()
