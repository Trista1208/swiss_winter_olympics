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
from multi_sport_qualification_checker import MultiSportQualificationChecker

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
        df = pd.read_csv("data/Results_Test_Version.csv", sep=';', encoding='utf-8')
        
        # Clean column names
        df.columns = df.columns.str.strip('"')
        
        # Convert date columns
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
        df['DoB'] = pd.to_datetime(df['DoB'], format='%Y/%m/%d %H:%M:%S', errors='coerce')
        
        # Clean rank column
        df['Rank_Clean'] = pd.to_numeric(df['Rank'].str.extract(r'(\d+)')[0], errors='coerce')
        
        # Add season column
        df['Season'] = df['Date'].apply(lambda x: f"{x.year-1}/{x.year}" if x.month <= 6 else f"{x.year}/{x.year+1}")
        
        # Filter for Swiss athletes only
        df = df[df['Nationality'] == 'SUI'].copy()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def get_athlete_qualification_status(athlete_name, df):
    """Get qualification status for an athlete across all sports"""
    try:
        athlete_data = df[df['Person'] == athlete_name]
        if athlete_data.empty:
            return None, "Athlete not found"
        
        # Initialize multi-sport checker
        checker = MultiSportQualificationChecker(df)
        
        # Get comprehensive qualification status
        result = checker.check_athlete_qualification(athlete_name)
        
        if 'error' in result:
            return None, result['error']
        
        return result, None
        
    except Exception as e:
        return None, f"Error checking qualification: {e}"

@st.cache_data  
def get_biathlon_qualification_status(athlete_name, df):
    """Get biathlon-specific qualification status (for backwards compatibility)"""
    try:
        # Get multi-sport status first
        multi_result, error = get_athlete_qualification_status(athlete_name, df)
        
        if error or not multi_result:
            return None, error or "No qualification data available"
        
        # Extract biathlon-specific information
        biathlon_qual = multi_result['sports_qualifications'].get('Biathlon')
        
        if not biathlon_qual:
            return None, "No biathlon qualification data"
        
        return {
            'is_qualified': biathlon_qual.get('qualified', False),
            'routes': biathlon_qual.get('routes', {}),
            'qualified_routes': biathlon_qual.get('qualified_routes', [])
        }, None
        
    except Exception as e:
        return None, f"Error checking biathlon qualification: {e}"

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
    
    # Determine qualification status for all sports
    multi_qualification_info = None
    qualification_error = None
    
    multi_qualification_info, qualification_error = get_athlete_qualification_status(athlete_name, df)
    
    # Keep backwards compatibility for biathlon-specific display
    qualification_info = None
    if 'Biathlon' in sports and multi_qualification_info:
        biathlon_qual = multi_qualification_info['sports_qualifications'].get('Biathlon')
        if biathlon_qual:
            qualification_info = {
                'is_qualified': biathlon_qual.get('qualified', False),
                'routes': biathlon_qual.get('routes', {}),
                'qualified_routes': biathlon_qual.get('qualified_routes', [])
            }
    
    # Determine result container class
    if qualification_info and qualification_info['is_qualified']:
        container_class = "athlete-result"
        status_badge_class = "qualified-badge"
        status_text = "🏅 QUALIFIED FOR MILANO CORTINA 2026 OLYMPICS"
        status_emoji = "✅"
    elif qualification_info and not qualification_info['is_qualified']:
        container_class = "athlete-result not-qualified-result"
        status_badge_class = "not-qualified-badge"
        status_text = "❌ NOT QUALIFIED FOR MILANO CORTINA 2026 OLYMPICS"
        status_emoji = "❌"
    else:
        container_class = "athlete-result no-qualification-result"
        status_badge_class = "no-data-badge"
        status_text = "ℹ️ NO BIATHLON QUALIFICATION DATA (Milano 2026)"
        status_emoji = "ℹ️"
    
    # Display athlete card
    with st.container():
        st.markdown(f"""
        <div class="{container_class}">
            <h2>{status_emoji} {athlete_name}</h2>
            <div class="qualification-status {status_badge_class}">
                {status_text}
            </div>
            <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                🏔️ <strong>Milano Cortina 2026 Winter Olympics</strong> - Swiss Team Selection Status
            </p>
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
        
        # Milano Cortina 2026 Olympic Qualification Status - ALL SPORTS
        st.subheader("🏔️ Milano Cortina 2026 Olympics - Qualification Status")
        
        if multi_qualification_info:
            # Overall status
            if multi_qualification_info['overall_qualified']:
                st.success("✅ **QUALIFIED FOR MILANO CORTINA 2026**")
                st.info(f"🏅 Qualified in: **{', '.join(multi_qualification_info['qualified_sports'])}**")
            else:
                st.error("❌ **NOT QUALIFIED FOR MILANO CORTINA 2026**")
                st.warning("⚠️ This athlete has not yet met Swiss Olympic qualification criteria in any sport.")
            
            st.write("---")
            st.write("### Sport-by-Sport Qualification Breakdown:")
            
            # Display each sport separately
            for sport, sport_qual in multi_qualification_info['sports_qualifications'].items():
                if isinstance(sport_qual, dict):
                    # Sport header with status
                    status_icon = "✅" if sport_qual.get('qualified', False) else "❌"
                    st.write(f"#### {status_icon} **{sport}**")
                    
                    if sport_qual.get('qualified', False):
                        qualified_routes = sport_qual.get('qualified_routes', [])
                        st.success(f"🏅 **QUALIFIED** via: {', '.join(qualified_routes)}")
                    else:
                        st.error("❌ **NOT QUALIFIED**")
                    
                    # Route details in expander
                    with st.expander(f"🔍 {sport} - Detailed Route Analysis", expanded=sport_qual.get('qualified', False)):
                        routes = sport_qual.get('routes', {})
                        
                        # Special handling for biathlon with route descriptions
                        if sport == 'Biathlon':
                            route_descriptions = {
                                "Route 1": "Top-3 at World Championships 2025 AND 1x Top-30 in World Cup 2025/26",
                                "Route 2": "1x Top-6 in World Cup 2024/25 AND 1x Top-25 in World Cup 2025/26", 
                                "Route 3": "1x Top-15 in World Cup 2025/26",
                                "Route 4": "2x Top-25 in World Cup 2025/26",
                                "Route 5": "1x Top-5 in IBU Cup 2025/26 AND 2x Top-30 in World Cup 2025/26"
                            }
                            st.write("*Swiss Olympic qualification routes for biathlon:*")
                            for route, qualified in routes.items():
                                status_icon = "✅" if qualified else "❌"
                                description = route_descriptions.get(route, "Unknown route")
                                status_text = "**QUALIFIED**" if qualified else "Not met"
                                st.write(f"{status_icon} **{route}** ({status_text}): {description}")
                        else:
                            # Generic route display for other sports
                            st.write(f"*Swiss Olympic qualification routes for {sport.lower()}:*")
                            for route, qualified in routes.items():
                                status_icon = "✅" if qualified else "❌"
                                status_text = "**QUALIFIED**" if qualified else "Not met"
                                st.write(f"{status_icon} **{route}**: {status_text}")
                        
                        if 'reason' in sport_qual:
                            st.info(f"ℹ️ {sport_qual['reason']}")
                    
                    st.write("")  # Add space between sports
        
        elif qualification_error:
            st.warning(f"⚠️ Could not determine qualification status: {qualification_error}")
        else:
            st.info("ℹ️ Qualification status could not be determined")
        
        # Recent results
        st.subheader("📅 Recent Results")
        recent_results = athlete_data.sort_values('Date', ascending=False).head(10)
        display_cols = ['Date', 'Sport', 'Competition', 'Discipline', 'Rank_Clean', 'Season']
        available_cols = [col for col in display_cols if col in recent_results.columns]
        st.dataframe(recent_results[available_cols], use_container_width=True)

def main():
    """Main application"""
    
    # Initialize session state
    if 'selected_athlete' not in st.session_state:
        st.session_state.selected_athlete = ""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Swiss Olympic Athlete Lookup</h1>', unsafe_allow_html=True)
    st.markdown("### 🏔️ Milano Cortina 2026 Olympics - Search athletes, filter by sport, and check qualification status")
    
    # Milano 2026 Info Banner
    st.info("🎿 **Milano Cortina 2026 Winter Olympics** | Search Swiss athletes and check their qualification status for the upcoming Winter Olympics in Italy (February 6-22, 2026)")
    
    # Load data
    with st.spinner("Loading Swiss Olympic athlete data..."):
        df = load_all_data()
    
    if df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Get all athletes
    all_athletes = sorted(df['Person'].dropna().unique())
    
    # Search interface
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        st.subheader("🔍 Search & Filter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_option = st.radio(
                "Search Method:",
                ["Type athlete name", "Select from dropdown"],
                horizontal=True
            )
            
            # Use session state for athlete selection
            if search_option == "Type athlete name":
                athlete_name = st.text_input(
                    "Enter athlete name:",
                    value=st.session_state.selected_athlete,
                    placeholder="e.g., Amy Baserga, Niklas Hartweg...",
                    help="Start typing an athlete's name",
                    key="athlete_input"
                )
                
                # Update session state when input changes
                if athlete_name != st.session_state.selected_athlete:
                    st.session_state.selected_athlete = athlete_name
                
                # Auto-suggest matching names
                if athlete_name and athlete_name not in all_athletes:
                    matching_athletes = [name for name in all_athletes if athlete_name.lower() in name.lower()]
                    if matching_athletes:
                        st.write("**Suggestions:**")
                        cols_suggest = st.columns(min(3, len(matching_athletes[:5])))
                        for i, match in enumerate(matching_athletes[:5]):
                            with cols_suggest[i % len(cols_suggest)]:
                                if st.button(f"🎯 {match}", key=f"suggest_{match}"):
                                    st.session_state.selected_athlete = match
                                    st.rerun()
            else:
                # Dropdown selection
                current_index = 0
                if st.session_state.selected_athlete in all_athletes:
                    current_index = all_athletes.index(st.session_state.selected_athlete) + 1
                
                selected_index = st.selectbox(
                    "Select athlete:",
                    range(len(all_athletes) + 1),
                    format_func=lambda x: "" if x == 0 else all_athletes[x-1],
                    index=current_index,
                    help="Choose an athlete from the dropdown"
                )
                
                if selected_index > 0:
                    athlete_name = all_athletes[selected_index - 1]
                    st.session_state.selected_athlete = athlete_name
                else:
                    athlete_name = ""
                    st.session_state.selected_athlete = ""
        
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
    
    # Use the selected athlete from session state
    current_athlete = st.session_state.selected_athlete
    
    # Search results
    if current_athlete and current_athlete.strip():
        # Check if athlete exists
        if current_athlete in all_athletes:
            display_athlete_info(current_athlete, df)
        else:
            st.error(f"❌ Athlete '{current_athlete}' not found in the database.")
            
            # Show similar names
            similar_names = [name for name in all_athletes if current_athlete.lower() in name.lower()]
            if similar_names:
                st.write("**Did you mean:**")
                cols_similar = st.columns(min(3, len(similar_names[:9])))
                for i, name in enumerate(similar_names[:9]):
                    with cols_similar[i % len(cols_similar)]:
                        if st.button(f"🔍 {name}", key=f"similar_{name}"):
                            st.session_state.selected_athlete = name
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
            
            # Show athletes in a more organized way
            athletes_per_page = 15
            total_pages = (len(athletes_to_show) - 1) // athletes_per_page + 1
            
            if total_pages > 1:
                page = st.selectbox("Page:", range(1, total_pages + 1), format_func=lambda x: f"Page {x}")
                start_idx = (page - 1) * athletes_per_page
                end_idx = min(start_idx + athletes_per_page, len(athletes_to_show))
                current_athletes = athletes_to_show[start_idx:end_idx]
            else:
                current_athletes = athletes_to_show
            
            # Show athletes in columns
            cols = st.columns(3)
            for i, athlete in enumerate(current_athletes):
                with cols[i % 3]:
                    if st.button(f"🔍 {athlete}", key=f"browse_{athlete}"):
                        st.session_state.selected_athlete = athlete
                        st.rerun()
        else:
            st.warning("No athletes found matching your filters.")
        
        # Milano 2026 Biathlon Team Status
        biathlon_df = df[df['Sport'] == 'Biathlon']
        if not biathlon_df.empty:
            st.subheader("🏔️ Milano Cortina 2026 - Swiss Biathlon Team Status")
            
            # Get qualification status for biathlon athletes
            qualified_count = 0
            biathlon_athletes = biathlon_df['Person'].unique()
            
            for athlete in biathlon_athletes:
                qual_info, _ = get_biathlon_qualification_status(athlete, df)
                if qual_info and qual_info['is_qualified']:
                    qualified_count += 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎿 Biathlon Athletes", len(biathlon_athletes))
            with col2:
                st.metric("✅ Qualified for Milano 2026", qualified_count)
            with col3:
                st.metric("❌ Not Yet Qualified", len(biathlon_athletes) - qualified_count)
            
            if qualified_count > 0:
                st.success(f"🏅 **{qualified_count} Swiss biathlon athletes have qualified for Milano Cortina 2026!**")
            
            st.info("💡 **Tip:** Filter by 'Biathlon' sport to see all biathlon athletes and their Milano 2026 qualification status.")
        
        # Quick stats
        st.subheader("📊 Database Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Athletes", len(df['Person'].unique()))
        with col2:
            st.metric("Sports Covered", len(df['Sport'].unique()))
        with col3:
            biathlon_athletes_count = len(df[df['Sport'] == 'Biathlon']['Person'].unique())
            st.metric("Biathlon Athletes", biathlon_athletes_count)
        with col4:
            st.metric("Total Results", len(df))

if __name__ == "__main__":
    main()
