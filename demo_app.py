import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the page
st.set_page_config(
    page_title="SHL Hockey Stats - Demo",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown('<h1 style="text-align: center; color: #1f77b4;">🏒 SHL Hockey Statistics - English Demo</h1>', unsafe_allow_html=True)

# Sidebar for filters
st.sidebar.header("🔧 Filters")

# Sample data
competitions = ["SHL", "HockeyAllsvenskan"]
seasons = ["2024/2025", "2023/2024", "2022/2023"]
teams = [
    {"name": "Frölunda HC", "shortName": "FHC"},
    {"name": "Skellefteå AIK", "shortName": "SKE"},
    {"name": "Luleå HF", "shortName": "LHF"},
    {"name": "Färjestad BK", "shortName": "FBK"}
]

# Filter controls
selected_competition = st.sidebar.selectbox("Competition", competitions, index=0)
selected_season = st.sidebar.selectbox("Season", seasons, index=0)

# Display current selection
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Selection:**")
st.sidebar.markdown(f"🏆 {selected_competition}")
st.sidebar.markdown(f"📅 {selected_season}")

# Database info
st.sidebar.markdown("---")
st.sidebar.markdown("**Database Info:**")
st.sidebar.markdown(f"🏒 4 teams")
st.sidebar.markdown(f"👤 120 players")
st.sidebar.markdown(f"🎮 52 games")
st.sidebar.markdown(f"⚽ 312 goals")
st.sidebar.markdown(f"⚠️ 156 penalties")

# Cache controls
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Update cache"):
    st.success("Cache updated!")

# Success message to show connection
st.markdown('<div style="background-color: #d4edda; color: #155724; padding: 0.5rem 1rem; border-radius: 5px; border: 1px solid #c3e6cb; margin-bottom: 1rem;">🔗 Connected to Neo4j database</div>', unsafe_allow_html=True)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏆 Teams", "👤 Players", "🏒 Games"])

with tab1:
    st.header(f"📊 {selected_competition} {selected_season} Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏒 Teams", 4)
    
    with col2:
        st.metric("🎮 Total games", "52")
    
    with col3:
        st.metric("⚽ Total goals", "312")
    
    with col4:
        st.metric("📈 Avg goals/game", "6.0")
    
    st.markdown("---")
    
    # Sample charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥅 Top scoring teams")
        sample_data = pd.DataFrame({
            'team': ['Frölunda HC', 'Skellefteå AIK', 'Luleå HF', 'Färjestad BK'],
            'goals_for': [85, 78, 73, 69]
        })
        fig = px.bar(
            x=sample_data['goals_for'],
            y=sample_data['team'],
            orientation='h',
            title="Goals scored this season",
            labels={'x': 'Goals', 'y': 'Team'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Standings (top 4)")
        standings_table = pd.DataFrame({
            'Team': ['Frölunda HC', 'Skellefteå AIK', 'Luleå HF', 'Färjestad BK'],
            'Points': [78, 71, 67, 62],
            'Wins': [25, 23, 21, 19],
            'Losses': [27, 29, 31, 33],
            'Goals For': [85, 78, 73, 69],
            'Goals Against': [72, 75, 78, 81]
        })
        st.dataframe(standings_table, use_container_width=True, hide_index=True)

with tab2:
    st.header(f"🏆 {selected_competition} {selected_season} Team Statistics")
    
    team_options = ["📊 All teams (Table)"] + [f"🏒 {team['name']}" for team in teams]
    selected_option = st.selectbox("Select view:", team_options)
    
    st.subheader("📊 Full standings")
    
    display_df = pd.DataFrame({
        'Pos': [1, 2, 3, 4],
        'Team': ['Frölunda HC', 'Skellefteå AIK', 'Luleå HF', 'Färjestad BK'],
        'GP': [52, 52, 52, 52],
        'W': [25, 23, 21, 19],
        'L': [27, 29, 31, 33],
        'GF': [85, 78, 73, 69],
        'GA': [72, 75, 78, 81],
        'GD': [13, 3, -5, -12],
        'P': [78, 71, 67, 62],
        'P/GP': [1.50, 1.37, 1.29, 1.19],
        'W%': [48.1, 44.2, 40.4, 36.5]
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab3:
    st.header(f"👤 {selected_competition} {selected_season} Player Statistics")
    
    # Player stats tabs
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🥅 Goal Scorers", "🎯 Assist Leaders", "⚠️ Penalties"])
    
    with sub_tab1:
        st.subheader("🥅 Top goal scorers")
        
        limit = st.slider("Number of players to show:", 5, 50, 15)
        
        scorers_df = pd.DataFrame({
            'Rank': [1, 2, 3, 4, 5],
            'Player': ['Erik Karlsson', 'Mika Zibanejad', 'Victor Hedman', 'Gabriel Landeskog', 'Elias Pettersson'],
            'Team': ['Frölunda HC', 'Skellefteå AIK', 'Luleå HF', 'Färjestad BK', 'Frölunda HC'],
            'Goals': [28, 25, 23, 21, 19],
            'Games': [52, 48, 50, 52, 45],
            'Goals/game': [0.54, 0.52, 0.46, 0.40, 0.42]
        })
        
        st.dataframe(scorers_df, use_container_width=True, hide_index=True)

with tab4:
    st.header(f"🏒 {selected_competition} {selected_season} Games")
    
    limit = st.slider("Number of games to show:", 5, 50, 20)
    
    games_df = pd.DataFrame({
        'Date': ['2024-03-15', '2024-03-14', '2024-03-13', '2024-03-12'],
        'Home Team': ['Frölunda HC', 'Skellefteå AIK', 'Luleå HF', 'Färjestad BK'],
        'Away Team': ['Färjestad BK', 'Luleå HF', 'Frölunda HC', 'Skellefteå AIK'],
        'Score': ['3-2', '4-1', '2-5', '1-3'],
        'Attendance': ['12,500', '8,200', '7,800', '9,100']
    })
    
    st.dataframe(games_df, use_container_width=True, hide_index=True)