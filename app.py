import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configure the page
st.set_page_config(
    page_title="SHL Hockey Stats",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

def get_competitions():
    """Get available competitions from the database"""
    # This would normally use the MCP tools, but for demo purposes returning static data
    return ["SHL"]

def get_seasons():
    """Get available seasons from the database"""
    # This would normally use the MCP tools, but for demo purposes returning static data
    return ["2023/2024", "2024/2025"]

def get_teams():
    """Get all teams from the database"""
    # This would normally use the MCP tools, but for demo purposes returning static data
    teams = [
        {"name": "Linköping HC", "shortName": "LHC"},
        {"name": "Örebro HK", "shortName": "ÖHK"},
        {"name": "Brynäs IF", "shortName": "BIF"},
        {"name": "Färjestad BK", "shortName": "FBK"},
        {"name": "Växjö Lakers HC", "shortName": "VÄX"},
        {"name": "Skellefteå AIK", "shortName": "SKE"},
        {"name": "Luleå HF", "shortName": "LHF"},
        {"name": "IF Malmö Redhawks", "shortName": "MIF"},
        {"name": "Frölunda HC", "shortName": "FHC"},
        {"name": "HV 71", "shortName": "HV71"}
    ]
    return teams

def main():
    # Header
    st.markdown('<h1 class="main-header">🏒 SHL Hockey Statistics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for filters
    st.sidebar.header("🔧 Filters")
    
    # Get data for filters
    competitions = get_competitions()
    seasons = get_seasons()
    teams = get_teams()
    
    # Filter controls
    selected_competition = st.sidebar.selectbox("Competition", competitions, index=0)
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons)-1)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🏆 Teams", "👤 Players", "🏒 Games", "📈 Analysis"])
    
    with tab1:
        show_dashboard(selected_competition, selected_season)
    
    with tab2:
        show_teams(selected_competition, selected_season, teams)
    
    with tab3:
        show_players(selected_competition, selected_season)
    
    with tab4:
        show_games(selected_competition, selected_season)
    
    with tab5:
        show_analysis(selected_competition, selected_season)

def show_dashboard(competition, season):
    """Display the main dashboard with key statistics"""
    st.header(f"📊 {competition} {season} Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Games",
            value="456",
            delta="12 this week"
        )
    
    with col2:
        st.metric(
            label="Total Goals",
            value="2,847",
            delta="89 this week"
        )
    
    with col3:
        st.metric(
            label="Average Goals/Game",
            value="6.24",
            delta="0.12"
        )
    
    with col4:
        st.metric(
            label="Active Players",
            value="532",
            delta="-3"
        )
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Goals per Game Trend")
        # Sample data for demonstration
        dates = pd.date_range('2024-09-01', periods=30, freq='D')
        goals = np.random.poisson(6.2, 30)
        
        fig = px.line(
            x=dates,
            y=goals,
            title="Daily Goals Scored",
            labels={'x': 'Date', 'y': 'Goals'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Scoring Teams")
        # Sample data
        teams = ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"]
        goals = [156, 143, 139, 132, 128]
        
        fig = px.bar(
            x=goals,
            y=teams,
            orientation='h',
            title="Goals Scored This Season",
            labels={'x': 'Goals', 'y': 'Team'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def show_teams(competition, season, teams):
    """Display team statistics and standings"""
    st.header(f"🏆 {competition} {season} Team Statistics")
    
    # Team selector
    team_names = [team["name"] for team in teams]
    selected_team = st.selectbox("Select a team for detailed stats:", ["All Teams"] + team_names)
    
    if selected_team == "All Teams":
        show_standings(competition, season)
    else:
        show_team_details(selected_team, competition, season)

def show_standings(competition, season):
    """Display league standings"""
    st.subheader("Current Standings")
    
    # Sample standings data
    standings_data = {
        "Position": range(1, 11),
        "Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
        "Games": [25, 24, 25, 24, 25, 24, 25, 24, 25, 24],
        "Wins": [18, 17, 16, 15, 14, 12, 11, 9, 8, 6],
        "Losses": [7, 7, 9, 9, 11, 12, 14, 15, 17, 18],
        "Goals For": [156, 143, 139, 132, 128, 118, 112, 98, 89, 82],
        "Goals Against": [98, 103, 112, 118, 125, 134, 142, 156, 167, 178],
        "Goal Diff": [58, 40, 27, 14, 3, -16, -30, -58, -78, -96],
        "Points": [54, 51, 48, 45, 42, 36, 33, 27, 24, 18]
    }
    
    df_standings = pd.DataFrame(standings_data)
    
    # Style the dataframe
    styled_df = df_standings.style.format({
        'Goal Diff': lambda x: f"+{x}" if x > 0 else str(x)
    }).background_gradient(subset=['Points'], cmap='RdYlGn')
    
    st.dataframe(styled_df, use_container_width=True)

def show_team_details(team_name, competition, season):
    """Display detailed statistics for a specific team"""
    st.subheader(f"{team_name} - Detailed Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Games Played", "25")
        st.metric("Wins", "16")
        st.metric("Losses", "9")
    
    with col2:
        st.metric("Goals For", "139")
        st.metric("Goals Against", "112")
        st.metric("Goal Difference", "+27")
    
    with col3:
        st.metric("Points", "48")
        st.metric("Position", "3rd")
        st.metric("Points/Game", "1.92")
    
    # Recent form chart
    st.subheader("Recent Form (Last 10 Games)")
    recent_results = ["W", "W", "L", "W", "W", "L", "W", "W", "W", "L"]
    colors = ["green" if x == "W" else "red" for x in recent_results]
    
    fig = go.Figure(data=go.Bar(
        x=list(range(1, 11)),
        y=[1]*10,
        marker_color=colors,
        text=recent_results,
        textposition="middle center"
    ))
    fig.update_layout(
        title="Recent Results",
        xaxis_title="Game",
        yaxis_title="",
        showlegend=False,
        yaxis=dict(showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True)

def show_players(competition, season):
    """Display player statistics"""
    st.header(f"👤 {competition} {season} Player Statistics")
    
    # Player stats tabs
    ptab1, ptab2, ptab3 = st.tabs(["🥅 Top Scorers", "🎯 Assists Leaders", "⚠️ Penalty Leaders"])
    
    with ptab1:
        show_top_scorers()
    
    with ptab2:
        show_assists_leaders()
    
    with ptab3:
        show_penalty_leaders()

def show_top_scorers():
    """Display top goal scorers"""
    st.subheader("Leading Goal Scorers")
    
    # Sample data
    scorers_data = {
        "Rank": range(1, 11),
        "Player": ["Erik Gustafsson", "Lucas Raymond", "Alexander Holtz", "William Nylander", 
                  "Filip Forsberg", "Mika Zibanejad", "Gabriel Landeskog", "Victor Hedman",
                  "Elias Pettersson", "Rasmus Dahlin"],
        "Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
        "Games": [25, 24, 25, 24, 25, 24, 25, 24, 25, 24],
        "Goals": [23, 21, 19, 18, 17, 16, 15, 14, 13, 12],
        "Goals/Game": [0.92, 0.88, 0.76, 0.75, 0.68, 0.67, 0.60, 0.58, 0.52, 0.50]
    }
    
    df_scorers = pd.DataFrame(scorers_data)
    st.dataframe(df_scorers, use_container_width=True)

def show_assists_leaders():
    """Display top assist leaders"""
    st.subheader("Leading Assist Providers")
    
    # Sample data
    assists_data = {
        "Rank": range(1, 11),
        "Player": ["Victor Hedman", "Erik Gustafsson", "Rasmus Dahlin", "Mika Zibanejad",
                  "Gabriel Landeskog", "Lucas Raymond", "William Nylander", "Alexander Holtz",
                  "Filip Forsberg", "Elias Pettersson"],
        "Team": ["Brynäs IF", "Frölunda HC", "IF Malmö Redhawks", "Linköping HC", "HV 71",
                "Skellefteå AIK", "Färjestad BK", "Växjö Lakers", "Luleå HF", "Örebro HK"],
        "Games": [24, 25, 24, 24, 25, 24, 24, 25, 25, 25],
        "Assists": [32, 29, 27, 25, 24, 23, 22, 21, 20, 19],
        "Assists/Game": [1.33, 1.16, 1.13, 1.04, 0.96, 0.96, 0.92, 0.84, 0.80, 0.76]
    }
    
    df_assists = pd.DataFrame(assists_data)
    st.dataframe(df_assists, use_container_width=True)

def show_penalty_leaders():
    """Display penalty leaders"""
    st.subheader("Most Penalized Players")
    
    # Sample data
    penalty_data = {
        "Rank": range(1, 11),
        "Player": ["Tom Wilson", "Brad Marchand", "Patrice Bergeron", "Connor McDavid",
                  "Leon Draisaitl", "Nathan MacKinnon", "Auston Matthews", "Mikko Rantanen",
                  "Sidney Crosby", "Alex Ovechkin"],
        "Team": ["Brynäs IF", "Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK",
                "Luleå HF", "Linköping HC", "HV 71", "Örebro HK", "IF Malmö Redhawks"],
        "Games": [25, 24, 25, 24, 25, 24, 25, 24, 25, 24],
        "Penalties": [45, 42, 38, 35, 33, 31, 29, 27, 25, 23],
        "Penalty Minutes": [90, 84, 76, 70, 66, 62, 58, 54, 50, 46]
    }
    
    df_penalties = pd.DataFrame(penalty_data)
    st.dataframe(df_penalties, use_container_width=True)

def show_games(competition, season):
    """Display game results and schedules"""
    st.header(f"🏒 {competition} {season} Games")
    
    # Game tabs
    gtab1, gtab2 = st.tabs(["📅 Recent Games", "🔮 Upcoming Games"])
    
    with gtab1:
        show_recent_games()
    
    with gtab2:
        show_upcoming_games()

def show_recent_games():
    """Display recent game results"""
    st.subheader("Recent Game Results")
    
    # Sample game data
    games_data = {
        "Date": ["2024-12-10", "2024-12-09", "2024-12-08", "2024-12-07", "2024-12-06"],
        "Home Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"],
        "Away Team": ["Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
        "Score": ["4-2", "3-1", "5-3", "2-4", "1-2"],
        "Attendance": [12500, 8900, 11200, 9800, 7600]
    }
    
    df_games = pd.DataFrame(games_data)
    st.dataframe(df_games, use_container_width=True)

def show_upcoming_games():
    """Display upcoming games"""
    st.subheader("Upcoming Games")
    
    # Sample upcoming games
    upcoming_data = {
        "Date": ["2024-12-12", "2024-12-13", "2024-12-14", "2024-12-15", "2024-12-16"],
        "Time": ["19:00", "18:00", "19:30", "19:00", "18:30"],
        "Home Team": ["Brynäs IF", "Örebro HK", "IF Malmö Redhawks", "HV 71", "Växjö Lakers"],
        "Away Team": ["Frölunda HC", "Skellefteå AIK", "Linköping HC", "Färjestad BK", "Luleå HF"],
        "Venue": ["Gavlerinken", "Behrn Arena", "Malmö Arena", "Kinnarps Arena", "Vida Arena"]
    }
    
    df_upcoming = pd.DataFrame(upcoming_data)
    st.dataframe(df_upcoming, use_container_width=True)

def show_analysis(competition, season):
    """Display advanced analytics and comparisons"""
    st.header(f"📈 {competition} Advanced Analysis")
    
    # Analysis tabs
    atab1, atab2, atab3 = st.tabs(["📊 Team Comparison", "📈 Trends", "🎯 Performance Metrics"])
    
    with atab1:
        show_team_comparison()
    
    with atab2:
        show_trends_analysis()
    
    with atab3:
        show_performance_metrics()

def show_team_comparison():
    """Display team comparison charts"""
    st.subheader("Team Performance Comparison")
    
    # Sample comparison data
    teams = ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"]
    goals_for = [156, 143, 139, 132, 128]
    goals_against = [98, 103, 112, 118, 125]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Goals For', x=teams, y=goals_for))
    fig.add_trace(go.Bar(name='Goals Against', x=teams, y=goals_against))
    
    fig.update_layout(
        title="Goals For vs Goals Against - Top 5 Teams",
        xaxis_title="Team",
        yaxis_title="Goals",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_trends_analysis():
    """Display trends over time"""
    st.subheader("Season Trends")
    
    # Sample trend data
    weeks = list(range(1, 16))
    frölunda_points = np.cumsum(np.random.choice([0, 1, 2, 3], 15, p=[0.1, 0.2, 0.4, 0.3]))
    skelleftea_points = np.cumsum(np.random.choice([0, 1, 2, 3], 15, p=[0.15, 0.25, 0.35, 0.25]))
    växjö_points = np.cumsum(np.random.choice([0, 1, 2, 3], 15, p=[0.2, 0.3, 0.3, 0.2]))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=frölunda_points, mode='lines+markers', name='Frölunda HC'))
    fig.add_trace(go.Scatter(x=weeks, y=skelleftea_points, mode='lines+markers', name='Skellefteå AIK'))
    fig.add_trace(go.Scatter(x=weeks, y=växjö_points, mode='lines+markers', name='Växjö Lakers'))
    
    fig.update_layout(
        title="Points Accumulation Over Season",
        xaxis_title="Week",
        yaxis_title="Total Points"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_performance_metrics():
    """Display advanced performance metrics"""
    st.subheader("Advanced Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Shot efficiency
        teams = ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"]
        shot_efficiency = [12.5, 11.8, 11.2, 10.9, 10.6]
        
        fig = px.bar(
            x=teams,
            y=shot_efficiency,
            title="Shooting Efficiency (%)",
            labels={'x': 'Team', 'y': 'Shooting %'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Power play efficiency
        pp_efficiency = [23.5, 22.1, 21.8, 20.9, 19.7]
        
        fig = px.bar(
            x=teams,
            y=pp_efficiency,
            title="Power Play Efficiency (%)",
            labels={'x': 'Team', 'y': 'PP %'}
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
