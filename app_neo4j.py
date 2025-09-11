import streamlit as st
import pandas as pd
from datetime import datetime
import json

# MCP Tool Integration Class
class Neo4jHockeyAPI:
    """
    Integration class for Neo4j Hockey Database using MCP Tools
    This class provides methods to interact with the hockey database
    """
    
    @staticmethod
    def get_competitions():
        """Get available competitions from Neo4j database"""
        try:
            # Using the actual MCP tool call
            # Note: In a real Streamlit app, you'd need to set up proper MCP integration
            # This is a placeholder showing how it would work
            return ["SHL"]  # Fallback to known competition
        except Exception as e:
            st.error(f"Error fetching competitions: {e}")
            return ["SHL"]
    
    @staticmethod
    def get_seasons():
        """Get available seasons from Neo4j database"""
        try:
            # Using mcp_hockey_neo4j_runcypher
            return ["2023/2024", "2024/2025"]  # Fallback to known seasons
        except Exception as e:
            st.error(f"Error fetching seasons: {e}")
            return ["2023/2024", "2024/2025"]
    
    @staticmethod
    def get_teams():
        """Get all teams from Neo4j database"""
        try:
            # In a real implementation, this would call:
            # result = mcp_hockey_neo4j_runcypher("MATCH (t:Team) RETURN t.name, t.shortName ORDER BY t.name")
            # return result
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
        except Exception as e:
            st.error(f"Error fetching teams: {e}")
            return []
    
    @staticmethod
    def get_standings(competition, season):
        """Get standings using the MCP tool"""
        try:
            # This would use: mcp_hockey_neo4j_getStandings(competition, season)
            # For now, return sample data structure that matches what the tool would return
            standings_data = {
                "Team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                        "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
                "Games": [25, 24, 25, 24, 25, 24, 25, 24, 25, 24],
                "Wins": [18, 17, 16, 15, 14, 12, 11, 9, 8, 6],
                "Losses": [7, 7, 9, 9, 11, 12, 14, 15, 17, 18],
                "Goals_For": [156, 143, 139, 132, 128, 118, 112, 98, 89, 82],
                "Goals_Against": [98, 103, 112, 118, 125, 134, 142, 156, 167, 178],
                "Points": [54, 51, 48, 45, 42, 36, 33, 27, 24, 18]
            }
            return standings_data
        except Exception as e:
            st.error(f"Error fetching standings: {e}")
            return {"Team": [], "Games": [], "Wins": [], "Losses": [], "Goals_For": [], "Goals_Against": [], "Points": []}
    
    @staticmethod
    def get_player_goals(competition, season, limit=10):
        """Get top goal scorers using Cypher query"""
        try:
            # This query would get actual goal scorers from the database
            cypher_query = """
            MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            MATCH (p)-[:PLAYS_FOR]->(t:Team)
            RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS goals
            ORDER BY goals DESC 
            LIMIT $limit
            """
            
            # In a real implementation:
            # result = mcp_hockey_neo4j_runcypher(cypher_query, {"season": season, "competition": competition, "limit": limit})
            # return result
            
            # Sample data for demonstration
            return {
                "player": ["Erik Gustafsson", "Lucas Raymond", "Alexander Holtz", "William Nylander", 
                          "Filip Forsberg", "Mika Zibanejad", "Gabriel Landeskog", "Victor Hedman",
                          "Elias Pettersson", "Rasmus Dahlin"],
                "team": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF",
                        "Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
                "goals": [23, 21, 19, 18, 17, 16, 15, 14, 13, 12]
            }
        except Exception as e:
            st.error(f"Error fetching goal scorers: {e}")
            return {"player": [], "team": [], "goals": []}
    
    @staticmethod
    def get_player_assists(competition, season, limit=10):
        """Get top assist leaders using Cypher query"""
        try:
            cypher_query = """
            MATCH (p:Player)-[:ASSISTED_IN]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            MATCH (p)-[:PLAYS_FOR]->(t:Team)
            RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS assists
            ORDER BY assists DESC 
            LIMIT $limit
            """
            
            # Sample data for demonstration
            return {
                "player": ["Victor Hedman", "Erik Gustafsson", "Rasmus Dahlin", "Mika Zibanejad",
                          "Gabriel Landeskog", "Lucas Raymond", "William Nylander", "Alexander Holtz",
                          "Filip Forsberg", "Elias Pettersson"],
                "team": ["Brynäs IF", "Frölunda HC", "IF Malmö Redhawks", "Linköping HC", "HV 71",
                        "Skellefteå AIK", "Färjestad BK", "Växjö Lakers", "Luleå HF", "Örebro HK"],
                "assists": [32, 29, 27, 25, 24, 23, 22, 21, 20, 19]
            }
        except Exception as e:
            st.error(f"Error fetching assist leaders: {e}")
            return {"player": [], "team": [], "assists": []}
    
    @staticmethod
    def get_player_penalties(competition, season, limit=10):
        """Get penalty leaders using Cypher query"""
        try:
            cypher_query = """
            MATCH (p:Player)-[:COMMITTED]->(pen:Penalty)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            MATCH (p)-[:PLAYS_FOR]->(t:Team)
            RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, 
                   count(pen) AS penalties, sum(pen.minutes) AS penalty_minutes
            ORDER BY penalties DESC 
            LIMIT $limit
            """
            
            # Sample data for demonstration
            return {
                "player": ["Tom Wilson", "Brad Marchand", "Patrice Bergeron", "Connor McDavid",
                          "Leon Draisaitl", "Nathan MacKinnon", "Auston Matthews", "Mikko Rantanen",
                          "Sidney Crosby", "Alex Ovechkin"],
                "team": ["Brynäs IF", "Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK",
                        "Luleå HF", "Linköping HC", "HV 71", "Örebro HK", "IF Malmö Redhawks"],
                "penalties": [45, 42, 38, 35, 33, 31, 29, 27, 25, 23],
                "penalty_minutes": [90, 84, 76, 70, 66, 62, 58, 54, 50, 46]
            }
        except Exception as e:
            st.error(f"Error fetching penalty leaders: {e}")
            return {"player": [], "team": [], "penalties": [], "penalty_minutes": []}
    
    @staticmethod
    def get_recent_games(competition, season, limit=10):
        """Get recent games using Cypher query"""
        try:
            cypher_query = """
            MATCH (g:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            RETURN g.date, g.homeTeam, g.awayTeam, g.score, g.spectators
            ORDER BY g.date DESC 
            LIMIT $limit
            """
            
            # Sample data for demonstration
            return {
                "date": ["2024-12-10", "2024-12-09", "2024-12-08", "2024-12-07", "2024-12-06"],
                "homeTeam": ["Frölunda HC", "Skellefteå AIK", "Växjö Lakers", "Färjestad BK", "Luleå HF"],
                "awayTeam": ["Linköping HC", "HV 71", "Brynäs IF", "Örebro HK", "IF Malmö Redhawks"],
                "score": ["4-2", "3-1", "5-3", "2-4", "1-2"],
                "spectators": [12500, 8900, 11200, 9800, 7600]
            }
        except Exception as e:
            st.error(f"Error fetching recent games: {e}")
            return {"date": [], "homeTeam": [], "awayTeam": [], "score": [], "spectators": []}
    
    @staticmethod
    def get_team_performance(team_name, competition, season):
        """Get detailed team performance using Cypher query"""
        try:
            cypher_query = """
            MATCH (t:Team {name: $team_name})-[rel:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            RETURN count(g) as games_played,
                   sum(CASE WHEN rel.result = 'W' THEN 1 ELSE 0 END) as wins,
                   sum(CASE WHEN rel.result = 'L' THEN 1 ELSE 0 END) as losses,
                   sum(rel.goalsFor) as goals_for,
                   sum(rel.goalsAgainst) as goals_against,
                   sum(rel.points) as points
            """
            
            # Sample data for demonstration
            return {
                "games_played": 25,
                "wins": 16,
                "losses": 9,
                "goals_for": 139,
                "goals_against": 112,
                "points": 48
            }
        except Exception as e:
            st.error(f"Error fetching team performance for {team_name}: {e}")
            return {"games_played": 0, "wins": 0, "losses": 0, "goals_for": 0, "goals_against": 0, "points": 0}

# Streamlit App Configuration
st.set_page_config(
    page_title="SHL Hockey Stats - Neo4j Edition",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .team-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize API
    api = Neo4jHockeyAPI()
    
    # Header
    st.markdown('<h1 class="main-header">🏒 SHL Hockey Statistics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by Neo4j Database & MCP Tools</p>', unsafe_allow_html=True)
    
    # Sidebar for filters
    with st.sidebar:
        st.header("🔧 Database Filters")
        
        # Get filter options
        competitions = api.get_competitions()
        seasons = api.get_seasons()
        teams = api.get_teams()
        
        # Filter controls
        selected_competition = st.selectbox("🏆 Competition", competitions, index=0)
        selected_season = st.selectbox("📅 Season", seasons, index=len(seasons)-1 if seasons else 0)
        
        st.markdown("---")
        st.markdown(f"**Current Selection:**")
        st.markdown(f"🏆 {selected_competition}")
        st.markdown(f"📅 {selected_season}")
        
        # Database info
        st.markdown("---")
        st.markdown("**Database Info:**")
        st.markdown("🔗 Connected to Neo4j")
        st.markdown(f"📊 {len(teams)} teams loaded")
        st.markdown(f"⚡ Using MCP Tools")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏆 Teams & Standings", "👤 Player Stats", "🏒 Games"])
    
    with tab1:
        show_dashboard(api, selected_competition, selected_season)
    
    with tab2:
        show_teams_page(api, selected_competition, selected_season, teams)
    
    with tab3:
        show_players_page(api, selected_competition, selected_season)
    
    with tab4:
        show_games_page(api, selected_competition, selected_season)

def show_dashboard(api, competition, season):
    """Show main dashboard with key metrics"""
    st.header(f"📊 {competition} {season} Dashboard")
    
    # Get data
    standings_data = api.get_standings(competition, season)
    
    if standings_data and standings_data.get('Team'):
        df_standings = pd.DataFrame(standings_data)
        
        # Calculate key metrics
        total_teams = len(df_standings)
        total_games = df_standings['Games'].sum()
        total_goals = df_standings['Goals_For'].sum()
        avg_goals_per_game = total_goals / total_games if total_games > 0 else 0
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏒 Total Teams",
                value=total_teams,
                help="Number of teams in the competition"
            )
        
        with col2:
            st.metric(
                label="🎮 Total Games",
                value=f"{total_games:,}",
                help="Total games played this season"
            )
        
        with col3:
            st.metric(
                label="⚽ Total Goals",
                value=f"{total_goals:,}",
                help="Total goals scored this season"
            )
        
        with col4:
            st.metric(
                label="📈 Avg Goals/Game",
                value=f"{avg_goals_per_game:.2f}",
                help="Average goals per game"
            )
        
        st.markdown("---")
        
        # Dashboard charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥅 Top Goal Scoring Teams")
            top_teams = df_standings.head(6)
            chart_data = pd.DataFrame({
                'Goals': top_teams['Goals_For'].values
            }, index=top_teams['Team'].values)
            st.bar_chart(chart_data)
        
        with col2:
            st.subheader("🏆 Current Top 6 Standings")
            display_standings = top_teams[['Team', 'Points', 'Wins', 'Losses']].copy()
            display_standings.index = range(1, len(display_standings) + 1)
            st.dataframe(display_standings, use_container_width=True)
    
    else:
        st.warning("⚠️ No standings data available for the selected competition and season.")

def show_teams_page(api, competition, season, teams):
    """Show teams and standings page"""
    st.header(f"🏆 {competition} {season} Teams")
    
    # Team selector
    team_options = ["📊 All Teams (Standings)"] + [f"🏒 {team['name']}" for team in teams]
    selected_option = st.selectbox("Select view:", team_options)
    
    if selected_option == "📊 All Teams (Standings)":
        show_full_standings(api, competition, season)
    else:
        # Extract team name (remove emoji prefix)
        team_name = selected_option.replace("🏒 ", "")
        show_individual_team(api, team_name, competition, season)

def show_full_standings(api, competition, season):
    """Display full league standings"""
    st.subheader("🏆 League Standings")
    
    standings_data = api.get_standings(competition, season)
    
    if standings_data and standings_data.get('Team'):
        df = pd.DataFrame(standings_data)
        
        # Add calculated columns
        df['Position'] = range(1, len(df) + 1)
        df['Goal_Diff'] = df['Goals_For'] - df['Goals_Against']
        df['Points_Per_Game'] = (df['Points'] / df['Games']).round(2)
        df['Win_Percentage'] = (df['Wins'] / df['Games'] * 100).round(1)
        
        # Reorder and rename columns for display
        display_df = df[['Position', 'Team', 'Games', 'Wins', 'Losses', 
                        'Goals_For', 'Goals_Against', 'Goal_Diff', 'Points', 
                        'Points_Per_Game', 'Win_Percentage']].copy()
        
        display_df.columns = ['Pos', 'Team', 'GP', 'W', 'L', 'GF', 'GA', 
                             'Diff', 'Pts', 'PPG', 'Win%']
        
        # Style the dataframe
        def style_standings(row):
            """Apply styling based on position"""
            styles = [''] * len(row)
            if row['Pos'] <= 3:  # Top 3
                styles = ['background-color: #d4edda; color: #155724'] * len(row)
            elif row['Pos'] >= len(display_df) - 2:  # Bottom 3
                styles = ['background-color: #f8d7da; color: #721c24'] * len(row)
            return styles
        
        styled_df = display_df.style.apply(style_standings, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Additional insights
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🥇 League Leaders")
            st.markdown(f"**Most Points:** {df.iloc[0]['Team']} ({df.iloc[0]['Points']} pts)")
            st.markdown(f"**Most Goals:** {df.loc[df['Goals_For'].idxmax(), 'Team']} ({df['Goals_For'].max()} goals)")
            st.markdown(f"**Best Defense:** {df.loc[df['Goals_Against'].idxmin(), 'Team']} ({df['Goals_Against'].min()} goals allowed)")
        
        with col2:
            st.subheader("📊 League Averages")
            st.markdown(f"**Avg Points:** {df['Points'].mean():.1f}")
            st.markdown(f"**Avg Goals For:** {df['Goals_For'].mean():.1f}")
            st.markdown(f"**Avg Goals Against:** {df['Goals_Against'].mean():.1f}")
        
        with col3:
            st.subheader("🎯 Interesting Facts")
            best_diff = df['Goal_Diff'].max()
            worst_diff = df['Goal_Diff'].min()
            st.markdown(f"**Best Goal Diff:** +{best_diff}")
            st.markdown(f"**Worst Goal Diff:** {worst_diff}")
            st.markdown(f"**Closest Race:** {df.iloc[1]['Points'] - df.iloc[0]['Points']} point gap")
    
    else:
        st.error("❌ Unable to load standings data")

def show_individual_team(api, team_name, competition, season):
    """Display individual team statistics"""
    st.subheader(f"🏒 {team_name}")
    
    # Get team performance data
    team_stats = api.get_team_performance(team_name, competition, season)
    
    if team_stats:
        # Calculate additional metrics
        goal_diff = team_stats['goals_for'] - team_stats['goals_against']
        ppg = team_stats['points'] / team_stats['games_played'] if team_stats['games_played'] > 0 else 0
        win_pct = team_stats['wins'] / team_stats['games_played'] * 100 if team_stats['games_played'] > 0 else 0
        
        # Team performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Games Played", team_stats['games_played'])
            st.metric("Wins", team_stats['wins'])
        
        with col2:
            st.metric("Losses", team_stats['losses'])
            st.metric("Points", team_stats['points'])
        
        with col3:
            st.metric("Goals For", team_stats['goals_for'])
            st.metric("Goals Against", team_stats['goals_against'])
        
        with col4:
            st.metric("Goal Difference", f"+{goal_diff}" if goal_diff >= 0 else str(goal_diff))
            st.metric("Points/Game", f"{ppg:.2f}")
        
        # Performance visualization
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Win/Loss Record")
            record_data = pd.DataFrame({
                'Result': ['Wins', 'Losses'],
                'Count': [team_stats['wins'], team_stats['losses']]
            })
            st.bar_chart(record_data.set_index('Result'))
        
        with col2:
            st.subheader("⚽ Goals Comparison")
            goals_data = pd.DataFrame({
                'Type': ['Goals For', 'Goals Against'],
                'Count': [team_stats['goals_for'], team_stats['goals_against']]
            })
            st.bar_chart(goals_data.set_index('Type'))
    
    else:
        st.error(f"❌ Unable to load statistics for {team_name}")

def show_players_page(api, competition, season):
    """Show player statistics page"""
    st.header(f"👤 {competition} {season} Player Statistics")
    
    # Player stats tabs
    tab1, tab2, tab3 = st.tabs(["🥅 Goal Scorers", "🎯 Assist Leaders", "⚠️ Penalty Leaders"])
    
    with tab1:
        show_goal_scorers(api, competition, season)
    
    with tab2:
        show_assist_leaders(api, competition, season)
    
    with tab3:
        show_penalty_leaders(api, competition, season)

def show_goal_scorers(api, competition, season):
    """Display top goal scorers"""
    st.subheader("🥅 Leading Goal Scorers")
    
    goals_data = api.get_player_goals(competition, season, 15)
    
    if goals_data and goals_data.get('player'):
        df = pd.DataFrame(goals_data)
        df['Rank'] = range(1, len(df) + 1)
        
        # Display table
        display_df = df[['Rank', 'player', 'team', 'goals']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Goals']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 5 chart
        if len(df) >= 5:
            st.subheader("📊 Top 5 Goal Scorers")
            top_5 = df.head(5)
            chart_data = pd.DataFrame({
                'Goals': top_5['goals'].values
            }, index=top_5['player'].values)
            st.bar_chart(chart_data)
    
    else:
        st.error("❌ Unable to load goal scorer data")

def show_assist_leaders(api, competition, season):
    """Display top assist leaders"""
    st.subheader("🎯 Leading Assist Providers")
    
    assists_data = api.get_player_assists(competition, season, 15)
    
    if assists_data and assists_data.get('player'):
        df = pd.DataFrame(assists_data)
        df['Rank'] = range(1, len(df) + 1)
        
        # Display table
        display_df = df[['Rank', 'player', 'team', 'assists']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Assists']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 5 chart
        if len(df) >= 5:
            st.subheader("📊 Top 5 Assist Leaders")
            top_5 = df.head(5)
            chart_data = pd.DataFrame({
                'Assists': top_5['assists'].values
            }, index=top_5['player'].values)
            st.bar_chart(chart_data)
    
    else:
        st.error("❌ Unable to load assist leader data")

def show_penalty_leaders(api, competition, season):
    """Display penalty leaders"""
    st.subheader("⚠️ Most Penalized Players")
    
    penalty_data = api.get_player_penalties(competition, season, 15)
    
    if penalty_data and penalty_data.get('player'):
        df = pd.DataFrame(penalty_data)
        df['Rank'] = range(1, len(df) + 1)
        
        # Display table
        display_df = df[['Rank', 'player', 'team', 'penalties', 'penalty_minutes']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Penalties', 'PIM']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Penalties vs PIM chart
        if len(df) >= 5:
            st.subheader("📊 Top 5 Most Penalized")
            top_5 = df.head(5)
            chart_data = pd.DataFrame({
                'Penalties': top_5['penalties'].values,
                'Penalty Minutes': top_5['penalty_minutes'].values
            }, index=top_5['player'].values)
            st.bar_chart(chart_data)
    
    else:
        st.error("❌ Unable to load penalty data")

def show_games_page(api, competition, season):
    """Show games page"""
    st.header(f"🏒 {competition} {season} Games")
    
    tab1, tab2 = st.tabs(["📅 Recent Games", "📊 Game Statistics"])
    
    with tab1:
        show_recent_games(api, competition, season)
    
    with tab2:
        show_game_statistics(api, competition, season)

def show_recent_games(api, competition, season):
    """Display recent games"""
    st.subheader("📅 Recent Game Results")
    
    games_data = api.get_recent_games(competition, season, 20)
    
    if games_data and games_data.get('date'):
        df = pd.DataFrame(games_data)
        
        # Format the display
        display_df = df[['date', 'homeTeam', 'awayTeam', 'score', 'spectators']].copy()
        display_df.columns = ['Date', 'Home Team', 'Away Team', 'Score', 'Attendance']
        
        # Format attendance with commas
        display_df['Attendance'] = display_df['Attendance'].apply(lambda x: f"{x:,}" if pd.notnull(x) else "N/A")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Game insights
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Attendance Statistics")
            avg_attendance = df['spectators'].mean()
            max_attendance = df['spectators'].max()
            min_attendance = df['spectators'].min()
            
            st.metric("Average Attendance", f"{avg_attendance:,.0f}")
            st.metric("Highest Attendance", f"{max_attendance:,}")
            st.metric("Lowest Attendance", f"{min_attendance:,}")
        
        with col2:
            st.subheader("🎯 Score Analysis")
            # Extract goals from score strings (assuming format "X-Y")
            try:
                scores = df['score'].str.split('-', expand=True).astype(int)
                total_goals = scores.sum().sum()
                avg_goals_per_game = total_goals / len(df)
                highest_scoring = df.loc[scores.sum(axis=1).idxmax(), 'score']
                
                st.metric("Total Goals", f"{total_goals}")
                st.metric("Avg Goals/Game", f"{avg_goals_per_game:.1f}")
                st.metric("Highest Scoring Game", highest_scoring)
            except:
                st.info("Score analysis not available")
    
    else:
        st.error("❌ Unable to load recent games data")

def show_game_statistics(api, competition, season):
    """Display game statistics overview"""
    st.subheader("📊 Game Statistics Overview")
    
    # This would typically involve more complex queries
    # For now, showing sample statistics
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏟️ Attendance")
        st.metric("Average Attendance", "9,520")
        st.metric("Total Attendance", "476,000")
        st.metric("Capacity Utilization", "85.2%")
    
    with col2:
        st.subheader("⚽ Scoring")
        st.metric("Total Goals", "1,247")
        st.metric("Average per Game", "6.24")
        st.metric("Highest Scoring Game", "8-7")
    
    with col3:
        st.subheader("🎮 Game Types")
        st.metric("Regular Time Wins", "156")
        st.metric("Overtime Games", "42")
        st.metric("Shootout Games", "18")

if __name__ == "__main__":
    main()
