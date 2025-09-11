import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# Note: The MCP tools would be called here in a real implementation
# For now, we'll create wrapper functions that simulate the database calls

class HockeyDataService:
    """Service class to handle all database interactions"""
    
    @staticmethod
    def get_competitions():
        """Get available competitions from Neo4j database"""
        # In real implementation, this would call:
        # mcp_hockey_neo4j_runcypher("MATCH (c:Competition) RETURN c.name ORDER BY c.name")
        return ["SHL"]
    
    @staticmethod
    def get_seasons():
        """Get available seasons from Neo4j database"""
        # In real implementation, this would call:
        # mcp_hockey_neo4j_runcypher("MATCH (s:Season) RETURN s.name ORDER BY s.name")
        return ["2023/2024", "2024/2025"]
    
    @staticmethod
    def get_teams():
        """Get all teams from Neo4j database"""
        # In real implementation, this would call:
        # mcp_hockey_neo4j_runcypher("MATCH (t:Team) RETURN t.name, t.shortName ORDER BY t.name")
        return [
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
    
    @staticmethod
    def get_standings(competition, season):
        """Get standings for a specific competition and season"""
        # In real implementation, this would call:
        # mcp_hockey_neo4j_getStandings(competition, season)
        return {
            "Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                    "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
            "Games": [25, 24, 25, 24, 25, 24, 25, 24, 25, 24],
            "Wins": [18, 17, 16, 15, 14, 12, 11, 9, 8, 6],
            "Losses": [7, 7, 9, 9, 11, 12, 14, 15, 17, 18],
            "Goals_For": [156, 143, 139, 132, 128, 118, 112, 98, 89, 82],
            "Goals_Against": [98, 103, 112, 118, 125, 134, 142, 156, 167, 178],
            "Points": [54, 51, 48, 45, 42, 36, 33, 27, 24, 18]
        }
    
    @staticmethod
    def get_top_scorers(competition, season, limit=10):
        """Get top goal scorers for a specific competition and season"""
        # In real implementation, this would call a Cypher query like:
        # """
        # MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        # MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        # MATCH (p)-[:PLAYS_FOR]->(t:Team)
        # RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS goals
        # ORDER BY goals DESC LIMIT $limit
        # """
        return {
            "Player": ["Erik Gustafsson", "Lucas Raymond", "Alexander Holtz", "William Nylander", 
                      "Filip Forsberg", "Mika Zibanejad", "Gabriel Landeskog", "Victor Hedman",
                      "Elias Pettersson", "Rasmus Dahlin"],
            "Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                    "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
            "Goals": [23, 21, 19, 18, 17, 16, 15, 14, 13, 12]
        }
    
    @staticmethod
    def get_top_assists(competition, season, limit=10):
        """Get top assist leaders for a specific competition and season"""
        # In real implementation, this would call a Cypher query like:
        # """
        # MATCH (p:Player)-[:ASSISTED_IN]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        # MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        # MATCH (p)-[:PLAYS_FOR]->(t:Team)
        # RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS assists
        # ORDER BY assists DESC LIMIT $limit
        # """
        return {
            "Player": ["Victor Hedman", "Erik Gustafsson", "Rasmus Dahlin", "Mika Zibanejad",
                      "Gabriel Landeskog", "Lucas Raymond", "William Nylander", "Alexander Holtz",
                      "Filip Forsberg", "Elias Pettersson"],
            "Team": ["Brynäs IF", "Frölunda HC", "IF Malmö Redhawks", "Linköping HC", "HV 71",
                    "Skellefteå AIK", "Färjestad BK", "Växjö Lakers", "Luleå HF", "Örebro HK"],
            "Assists": [32, 29, 27, 25, 24, 23, 22, 21, 20, 19]
        }
    
    @staticmethod
    def get_penalty_leaders(competition, season, limit=10):
        """Get penalty leaders for a specific competition and season"""
        # In real implementation, this would call a Cypher query like:
        # """
        # MATCH (p:Player)-[:COMMITTED]->(pen:Penalty)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        # MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        # MATCH (p)-[:PLAYS_FOR]->(t:Team)
        # RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, 
        #        count(pen) AS penalties, sum(pen.minutes) AS penalty_minutes
        # ORDER BY penalties DESC LIMIT $limit
        # """
        return {
            "Player": ["Tom Wilson", "Brad Marchand", "Patrice Bergeron", "Connor McDavid",
                      "Leon Draisaitl", "Nathan MacKinnon", "Auston Matthews", "Mikko Rantanen",
                      "Sidney Crosby", "Alex Ovechkin"],
            "Team": ["Brynäs IF", "Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK",
                    "Luleå HF", "Linköping HC", "HV 71", "Örebro HK", "IF Malmö Redhawks"],
            "Penalties": [45, 42, 38, 35, 33, 31, 29, 27, 25, 23],
            "Penalty_Minutes": [90, 84, 76, 70, 66, 62, 58, 54, 50, 46]
        }
    
    @staticmethod
    def get_recent_games(competition, season, limit=10):
        """Get recent games for a specific competition and season"""
        # In real implementation, this would call a Cypher query like:
        # """
        # MATCH (g:Game)-[:PART_OF]->(s:Season {name: $season})
        # MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        # RETURN g.date, g.homeTeam, g.awayTeam, g.score, g.spectators
        # ORDER BY g.date DESC LIMIT $limit
        # """
        return {
            "Date": ["2024-12-10", "2024-12-09", "2024-12-08", "2024-12-07", "2024-12-06"],
            "Home_Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"],
            "Away_Team": ["Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
            "Score": ["4-2", "3-1", "5-3", "2-4", "1-2"],
            "Attendance": [12500, 8900, 11200, 9800, 7600]
        }
    
    @staticmethod
    def get_team_stats(team_name, competition, season):
        """Get detailed statistics for a specific team"""
        # In real implementation, this would call a complex Cypher query
        return {
            "games_played": 25,
            "wins": 16,
            "losses": 9,
            "goals_for": 139,
            "goals_against": 112,
            "goal_difference": 27,
            "points": 48,
            "position": 3,
            "points_per_game": 1.92
        }

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
    .team-logo {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize data service
    data_service = HockeyDataService()
    
    # Header
    st.markdown('<h1 class="main-header">🏒 SHL Hockey Statistics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for filters
    st.sidebar.header("🔧 Filters")
    
    # Get data for filters
    competitions = data_service.get_competitions()
    seasons = data_service.get_seasons()
    teams = data_service.get_teams()
    
    # Filter controls
    selected_competition = st.sidebar.selectbox("Competition", competitions, index=0)
    selected_season = st.sidebar.selectbox("Season", seasons, index=len(seasons)-1)
    
    # Display current selection info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Selected:** {selected_competition} {selected_season}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🏆 Teams", "👤 Players", "🏒 Games", "📈 Analysis"])
    
    with tab1:
        show_dashboard(data_service, selected_competition, selected_season)
    
    with tab2:
        show_teams(data_service, selected_competition, selected_season, teams)
    
    with tab3:
        show_players(data_service, selected_competition, selected_season)
    
    with tab4:
        show_games(data_service, selected_competition, selected_season)
    
    with tab5:
        show_analysis(data_service, selected_competition, selected_season)

def show_dashboard(data_service, competition, season):
    """Display the main dashboard with key statistics"""
    st.header(f"📊 {competition} {season} Overview")
    
    # Get standings for metrics
    standings_data = data_service.get_standings(competition, season)
    df_standings = pd.DataFrame(standings_data)
    
    # Calculate metrics
    total_games = df_standings['Games'].sum()
    total_goals = df_standings['Goals_For'].sum()
    avg_goals_per_game = total_goals / total_games if total_games > 0 else 0
    active_teams = len(df_standings)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Games",
            value=f"{total_games:,}",
            delta="Latest update"
        )
    
    with col2:
        st.metric(
            label="Total Goals",
            value=f"{total_goals:,}",
            delta=f"Across {active_teams} teams"
        )
    
    with col3:
        st.metric(
            label="Average Goals/Game",
            value=f"{avg_goals_per_game:.2f}",
            delta="Season average"
        )
    
    with col4:
        st.metric(
            label="Active Teams",
            value=f"{active_teams}",
            delta="Current season"
        )
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥅 Goals Scored by Team")
        
        # Create bar chart using Streamlit's built-in charting
        chart_data = pd.DataFrame({
            'Team': df_standings['Team'][:6],  # Top 6 teams
            'Goals': df_standings['Goals_For'][:6]
        }).set_index('Team')
        
        st.bar_chart(chart_data)
    
    with col2:
        st.subheader("📊 Current Standings (Top 6)")
        
        # Display top 6 teams in standings
        top_standings = df_standings.head(6)[['Team', 'Games', 'Wins', 'Losses', 'Points']]
        st.dataframe(
            top_standings,
            use_container_width=True,
            hide_index=True
        )

def show_teams(data_service, competition, season, teams):
    """Display team statistics and standings"""
    st.header(f"🏆 {competition} {season} Team Statistics")
    
    # Team selector
    team_names = [team["name"] for team in teams]
    selected_team = st.selectbox("Select a team for detailed stats:", ["All Teams"] + team_names)
    
    if selected_team == "All Teams":
        show_standings(data_service, competition, season)
    else:
        show_team_details(data_service, selected_team, competition, season)

def show_standings(data_service, competition, season):
    """Display league standings"""
    st.subheader("Current Standings")
    
    standings_data = data_service.get_standings(competition, season)
    df_standings = pd.DataFrame(standings_data)
    
    # Add calculated columns
    df_standings['Position'] = range(1, len(df_standings) + 1)
    df_standings['Goal_Diff'] = df_standings['Goals_For'] - df_standings['Goals_Against']
    df_standings['Win_Pct'] = (df_standings['Wins'] / df_standings['Games'] * 100).round(1)
    
    # Reorder columns for display
    display_columns = ['Position', 'Team', 'Games', 'Wins', 'Losses', 'Goals_For', 
                      'Goals_Against', 'Goal_Diff', 'Points', 'Win_Pct']
    df_display = df_standings[display_columns]
    
    # Rename columns for better display
    df_display.columns = ['Pos', 'Team', 'GP', 'W', 'L', 'GF', 'GA', 'Diff', 'Pts', 'Win%']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

def show_team_details(data_service, team_name, competition, season):
    """Display detailed statistics for a specific team"""
    st.subheader(f"{team_name} - Detailed Statistics")
    
    # Get team stats
    team_stats = data_service.get_team_stats(team_name, competition, season)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Games Played", team_stats['games_played'])
        st.metric("Wins", team_stats['wins'])
        st.metric("Losses", team_stats['losses'])
    
    with col2:
        st.metric("Goals For", team_stats['goals_for'])
        st.metric("Goals Against", team_stats['goals_against'])
        st.metric("Goal Difference", f"+{team_stats['goal_difference']}")
    
    with col3:
        st.metric("Points", team_stats['points'])
        st.metric("Position", f"{team_stats['position']}{'st' if team_stats['position'] == 1 else 'nd' if team_stats['position'] == 2 else 'rd' if team_stats['position'] == 3 else 'th'}")
        st.metric("Points/Game", f"{team_stats['points_per_game']:.2f}")
    
    # Recent form simulation
    st.subheader("Recent Form (Last 10 Games)")
    recent_results = ["W", "W", "L", "W", "W", "L", "W", "W", "W", "L"]
    
    # Display as colored boxes
    cols = st.columns(10)
    for i, result in enumerate(recent_results):
        with cols[i]:
            color = "🟢" if result == "W" else "🔴"
            st.markdown(f"<div style='text-align: center;'>{color}<br>{result}</div>", unsafe_allow_html=True)

def show_players(data_service, competition, season):
    """Display player statistics"""
    st.header(f"👤 {competition} {season} Player Statistics")
    
    # Player stats tabs
    ptab1, ptab2, ptab3 = st.tabs(["🥅 Top Scorers", "🎯 Assists Leaders", "⚠️ Penalty Leaders"])
    
    with ptab1:
        show_top_scorers(data_service, competition, season)
    
    with ptab2:
        show_assists_leaders(data_service, competition, season)
    
    with ptab3:
        show_penalty_leaders(data_service, competition, season)

def show_top_scorers(data_service, competition, season):
    """Display top goal scorers"""
    st.subheader("Leading Goal Scorers")
    
    scorers_data = data_service.get_top_scorers(competition, season)
    df_scorers = pd.DataFrame(scorers_data)
    df_scorers['Rank'] = range(1, len(df_scorers) + 1)
    
    # Reorder columns
    df_display = df_scorers[['Rank', 'Player', 'Team', 'Goals']]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Goals chart
    st.subheader("Goals Visualization")
    chart_data = pd.DataFrame({
        'Player': df_scorers['Player'][:5],  # Top 5
        'Goals': df_scorers['Goals'][:5]
    }).set_index('Player')
    
    st.bar_chart(chart_data)

def show_assists_leaders(data_service, competition, season):
    """Display top assist leaders"""
    st.subheader("Leading Assist Providers")
    
    assists_data = data_service.get_top_assists(competition, season)
    df_assists = pd.DataFrame(assists_data)
    df_assists['Rank'] = range(1, len(df_assists) + 1)
    
    # Reorder columns
    df_display = df_assists[['Rank', 'Player', 'Team', 'Assists']]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def show_penalty_leaders(data_service, competition, season):
    """Display penalty leaders"""
    st.subheader("Most Penalized Players")
    
    penalty_data = data_service.get_penalty_leaders(competition, season)
    df_penalties = pd.DataFrame(penalty_data)
    df_penalties['Rank'] = range(1, len(df_penalties) + 1)
    
    # Reorder columns
    df_display = df_penalties[['Rank', 'Player', 'Team', 'Penalties', 'Penalty_Minutes']]
    df_display.columns = ['Rank', 'Player', 'Team', 'Penalties', 'PIM']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def show_games(data_service, competition, season):
    """Display game results and schedules"""
    st.header(f"🏒 {competition} {season} Games")
    
    # Game tabs
    gtab1, gtab2 = st.tabs(["📅 Recent Games", "📊 Game Statistics"])
    
    with gtab1:
        show_recent_games(data_service, competition, season)
    
    with gtab2:
        show_game_statistics(data_service, competition, season)

def show_recent_games(data_service, competition, season):
    """Display recent game results"""
    st.subheader("Recent Game Results")
    
    games_data = data_service.get_recent_games(competition, season)
    df_games = pd.DataFrame(games_data)
    
    # Rename columns for better display
    df_games.columns = ['Date', 'Home Team', 'Away Team', 'Score', 'Attendance']
    
    st.dataframe(df_games, use_container_width=True, hide_index=True)

def show_game_statistics(data_service, competition, season):
    """Display game statistics"""
    st.subheader("Game Statistics Overview")
    
    # Sample statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Average Attendance", "9,520")
        st.metric("Highest Scoring Game", "8-7")
        st.metric("Most Goals in a Game", "15")
    
    with col2:
        st.metric("Lowest Scoring Game", "1-0")
        st.metric("Average Goals per Game", "6.24")
        st.metric("Overtime Games", "42")

def show_analysis(data_service, competition, season):
    """Display advanced analytics and comparisons"""
    st.header(f"📈 {competition} Advanced Analysis")
    
    # Analysis tabs
    atab1, atab2 = st.tabs(["📊 Team Comparison", "🎯 Performance Analysis"])
    
    with atab1:
        show_team_comparison(data_service, competition, season)
    
    with atab2:
        show_performance_analysis(data_service, competition, season)

def show_team_comparison(data_service, competition, season):
    """Display team comparison charts"""
    st.subheader("Team Performance Comparison")
    
    standings_data = data_service.get_standings(competition, season)
    df_standings = pd.DataFrame(standings_data)
    
    # Top 5 teams comparison
    top_5 = df_standings.head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Goals For vs Goals Against")
        comparison_data = pd.DataFrame({
            'Team': top_5['Team'],
            'Goals For': top_5['Goals_For'],
            'Goals Against': top_5['Goals_Against']
        }).set_index('Team')
        
        st.bar_chart(comparison_data)
    
    with col2:
        st.subheader("Win-Loss Record")
        record_data = pd.DataFrame({
            'Team': top_5['Team'],
            'Wins': top_5['Wins'],
            'Losses': top_5['Losses']
        }).set_index('Team')
        
        st.bar_chart(record_data)

def show_performance_analysis(data_service, competition, season):
    """Display performance analysis"""
    st.subheader("Performance Metrics")
    
    # Sample performance data
    teams = ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Offensive Efficiency")
        offensive_data = pd.DataFrame({
            'Team': teams,
            'Goals per Game': [6.24, 5.96, 5.56, 5.50, 5.12]
        }).set_index('Team')
        
        st.bar_chart(offensive_data)
    
    with col2:
        st.subheader("Defensive Performance")
        defensive_data = pd.DataFrame({
            'Team': teams,
            'Goals Against per Game': [3.92, 4.29, 4.48, 4.92, 5.00]
        }).set_index('Team')
        
        st.bar_chart(defensive_data)
    
    # Performance summary
    st.subheader("Key Performance Indicators")
    
    kpi_data = {
        "Metric": ["Best Offensive Team", "Best Defensive Team", "Most Consistent", "Best Home Record", "Best Away Record"],
        "Team": ["Frölunda HC", "Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK"],
        "Value": ["6.24 goals/game", "3.92 goals against/game", "±0.8 goal differential", "14-1 at home", "8-4 away"]
    }
    
    df_kpi = pd.DataFrame(kpi_data)
    st.dataframe(df_kpi, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
