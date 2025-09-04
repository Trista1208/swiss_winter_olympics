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

# Black theme CSS with high visibility
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
        border: 2px solid #333333;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Sidebar text */
    .css-1d391kg .stMarkdown {
        color: #ffffff;
    }
    
    /* Athlete cards */
    .athlete-card {
        background: #1a1a1a;
        border: 2px solid #333333;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .athlete-card:hover {
        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
        transform: translateY(-2px);
        border-color: #4ecdc4;
    }
    
    .athlete-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .athlete-details {
        color: #cccccc;
        margin-bottom: 0.5rem;
    }
    
    /* Qualification status badges */
    .qualification-status {
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    .qualified {
        background: #28a745;
        color: #ffffff;
        border: 1px solid #28a745;
    }
    
    .not-qualified {
        background: #dc3545;
        color: #ffffff;
        border: 1px solid #dc3545;
    }
    
    /* Stats container */
    .stats-container {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255,255,255,0.1);
        margin-bottom: 2rem;
        border: 2px solid #333333;
    }
    
    .stats-container h3 {
        color: #ffffff;
    }
    
    /* No results message */
    .no-results {
        text-align: center;
        color: #cccccc;
        font-style: italic;
        padding: 3rem;
        background: #1a1a1a;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255,255,255,0.1);
        border: 2px solid #333333;
    }
    
    /* Streamlit metric containers */
    div[data-testid="metric-container"] {
        background: #1a1a1a;
        border: 2px solid #333333;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(255,255,255,0.1);
    }
    
    div[data-testid="metric-container"] > div {
        color: #4ecdc4 !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #ffffff !important;
    }
    
    /* Streamlit dataframes */
    .stDataFrame {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 1rem;
        border: 2px solid #333333;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
    }
    
    .streamlit-expanderContent {
        background: #1a1a1a !important;
        border: 2px solid #333333 !important;
    }
    
    /* Text colors */
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
    }
    
    .stSelectbox select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #333333 !important;
    }
    
    .stMultiSelect {
        background-color: #1a1a1a !important;
    }
    
    /* Labels */
    .stTextInput label, .stSelectbox label, .stMultiSelect label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff !important;
    }
    
    /* Success/error colors on dark background */
    .stSuccess {
        background-color: #155724 !important;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: #721c24 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_sports_data():
    """Load and return the complete dataset"""
    try:
        # Load CSV with semicolon separator and clean column names
        df = pd.read_csv('data/Results_Test_Version.csv', sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip('"')
        
        # Filter for Swiss athletes only
        df = df[df['Nationality'] == 'SUI'].copy()
        
        # Clean and process the data
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        
        # Clean rank column - this is essential for qualification checker
        if 'Rank' in df.columns:
            df['Rank_Clean'] = df['Rank'].astype(str).str.extract(r'(\d+)')[0]
            df['Rank_Clean'] = pd.to_numeric(df['Rank_Clean'], errors='coerce')
        else:
            df['Rank_Clean'] = pd.Series([None] * len(df))
        
        # Use 'Person' column as 'Name' for consistency
        if 'Person' in df.columns:
            df['Name'] = df['Person']
        else:
            df['Name'] = pd.Series(['Unknown'] * len(df))
        
        # Keep both Gender columns for different purposes
        # PersonGender = athlete's personal gender (Women/Men)
        # Gender = competition gender category (Women/Men/Mixed)
        if 'PersonGender' not in df.columns:
            df['PersonGender'] = pd.Series(['Unknown'] * len(df))
        if 'Gender' not in df.columns:
            df['Gender'] = pd.Series(['Unknown'] * len(df))
        
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
                    
                    # Get qualification result using the checker's method
                    qual_result = _checker.check_athlete_qualification(athlete)
                    
                    # Check if athlete qualified for this specific sport
                    is_qualified = False
                    if qual_result and not qual_result.get('error'):
                        sport_qual = qual_result.get('sports_qualifications', {}).get(sport, {})
                        is_qualified = sport_qual.get('qualified', False)
                    
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
    
    # Count qualified routes from the sport qualification data
    qualified_routes = 0
    routes_info = athlete_info.get('routes', {})
    if routes_info and not routes_info.get('error'):
        sport_qual = routes_info.get('sports_qualifications', {}).get(sport, {})
        if sport_qual:
            qualified_routes = len(sport_qual.get('qualified_routes', []))
    
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

def display_detailed_athlete_profile(athlete_name, df, qualification_results):
    """Display comprehensive athlete profile with recent activities and qualification details"""
    
    st.markdown(f"""
    <div class="main-header">
        👤 {athlete_name} - Detailed Profile
    </div>
    """, unsafe_allow_html=True)
    
    # Get athlete's complete data
    athlete_data = df[df['Name'] == athlete_name].copy()
    
    if athlete_data.empty:
        st.error("No data found for this athlete")
        return
    
    # Basic info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = athlete_data['PersonGender'].iloc[0]
        nationality = athlete_data['Nationality'].iloc[0] if 'Nationality' in athlete_data.columns else 'N/A'
        st.metric("Gender", gender)
        st.metric("Nationality", nationality)
    
    with col2:
        sports_participated = athlete_data['Sport'].nunique()
        total_competitions = len(athlete_data)
        st.metric("Sports", sports_participated)
        st.metric("Total Competitions", total_competitions)
    
    with col3:
        # Overall qualification status
        total_qualified_sports = 0
        for sport, athletes in qualification_results.items():
            if athlete_name in athletes and athletes[athlete_name]['qualified']:
                total_qualified_sports += 1
        
        st.metric("Qualified Sports", f"{total_qualified_sports}/{sports_participated}")
        qualification_rate = (total_qualified_sports / sports_participated * 100) if sports_participated > 0 else 0
        st.metric("Qualification Rate", f"{qualification_rate:.1f}%")
    
    # Recent Activities by Sport
    st.markdown("### 🏅 Recent Activities by Sport")
    
    for sport in athlete_data['Sport'].unique():
        sport_data = athlete_data[athlete_data['Sport'] == sport].copy()
        sport_data = sport_data.sort_values('Date', ascending=False)
        
        with st.expander(f"🎿 {sport} ({len(sport_data)} competitions)", expanded=True):
            
            # Sport-specific qualification status
            is_qualified = False
            qualified_routes = []
            if sport in qualification_results and athlete_name in qualification_results[sport]:
                athlete_qual = qualification_results[sport][athlete_name]
                is_qualified = athlete_qual['qualified']
                
                # Get qualified routes
                routes_info = athlete_qual.get('routes', {})
                if routes_info and not routes_info.get('error'):
                    sport_qual = routes_info.get('sports_qualifications', {}).get(sport, {})
                    if sport_qual:
                        qualified_routes = sport_qual.get('qualified_routes', [])
            
            # Status display
            status_text = "✅ QUALIFIED for Milano 2026" if is_qualified else "❌ Not Qualified for Milano 2026"
            status_color = "green" if is_qualified else "red"
            st.markdown(f"**Status:** :{status_color}[{status_text}]")
            
            if qualified_routes:
                st.markdown(f"**Qualified via routes:** {', '.join(qualified_routes)}")
            
            # Recent competitions table
            st.markdown("**Recent Competitions:**")
            
            # Select relevant columns for display
            display_columns = ['Date', 'Competition', 'Discipline', 'Rank', 'Result']
            available_columns = [col for col in display_columns if col in sport_data.columns]
            
            if available_columns:
                recent_data = sport_data[available_columns].head(10)
                recent_data = recent_data.copy()
                
                # Format date if available
                if 'Date' in recent_data.columns:
                    recent_data['Date'] = recent_data['Date'].dt.strftime('%Y-%m-%d')
                
                st.dataframe(recent_data, use_container_width=True)
            
            # Performance statistics
            if 'Rank_Clean' in sport_data.columns:
                ranks = sport_data['Rank_Clean'].dropna()
                if not ranks.empty:
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Best Rank", int(ranks.min()))
                    with col_b:
                        st.metric("Average Rank", f"{ranks.mean():.1f}")
                    with col_c:
                        st.metric("Competitions", len(ranks))

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
    
    # Initialize qualification checker with dataframe
    checker = MultiSportQualificationChecker(df)
    
    # Get qualification results
    qualification_results, sport_summaries = get_multi_sport_qualification_results(checker, df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Search & Filter")
    
    # Get all available data
    all_sports = sorted(df['Sport'].unique()) if 'Sport' in df.columns else []
    all_athletes = sorted(df['Name'].unique()) if 'Name' in df.columns else []
    genders = sorted(df['PersonGender'].unique()) if 'PersonGender' in df.columns else []
    
    # Enhanced athlete selection
    st.sidebar.subheader("👤 Select Athlete")
    
    # Option 1: Search by typing
    search_name = st.sidebar.text_input("🔍 Search by Name:", placeholder="Type athlete name...")
    
    # Option 2: Select from dropdown
    selected_athlete = st.sidebar.selectbox(
        "📋 Or Select from List:",
        options=["None"] + all_athletes,
        index=0
    )
    
    # If an athlete is selected, show their detailed info
    if selected_athlete != "None" or search_name:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎯 Selected Athlete Details")
        
        # Determine which athlete to show
        target_athlete = selected_athlete if selected_athlete != "None" else search_name
        
        if target_athlete:
            athlete_data = df[df['Name'].str.contains(target_athlete, case=False, na=False)]
            if not athlete_data.empty:
                # Show athlete summary in sidebar
                athlete_sports = athlete_data['Sport'].unique()
                athlete_gender = athlete_data['Gender'].iloc[0]
                total_competitions = len(athlete_data)
                
                st.sidebar.write(f"**Name:** {target_athlete}")
                st.sidebar.write(f"**Gender:** {athlete_gender}")
                st.sidebar.write(f"**Sports:** {', '.join(athlete_sports)}")
                st.sidebar.write(f"**Total Competitions:** {total_competitions}")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏅 General Filters")
    
    # Filter by sport
    selected_sports = st.sidebar.multiselect(
        "🏅 Filter by Sport:",
        options=["All"] + all_sports,
        default=["All"]
    )
    
    # Filter by gender
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
    
    # Main content area - check if specific athlete is selected
    target_athlete = None
    if selected_athlete != "None":
        target_athlete = selected_athlete
    elif search_name:
        # Find exact match or best match
        matching_athletes = [name for name in all_athletes if search_name.lower() in name.lower()]
        if matching_athletes:
            target_athlete = matching_athletes[0]  # Take first match
    
    # If specific athlete is selected, show detailed profile
    if target_athlete:
        display_detailed_athlete_profile(target_athlete, df, qualification_results)
    else:
        # Show general overview with filters
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
                    # Name search filter (when not showing detailed profile)
                    if search_name and search_name.lower() not in athlete_name.lower():
                        continue
                    
                    # Gender filter - use PersonGender for athlete's actual gender
                    athlete_data = athlete_info['data'].iloc[0] if len(athlete_info['data']) > 0 else {}
                    athlete_gender = athlete_data.get('PersonGender', 'N/A')
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
                st.markdown("💡 **Tip:** Select an athlete from the sidebar to see detailed profile, recent activities, and qualification routes!")
                
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
