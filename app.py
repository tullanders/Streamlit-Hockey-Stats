import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import time
import logging

# Load environment variables from .env file
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="SHL Hockey Stats - Neo4j Live",
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
    .connection-status {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin-bottom: 1rem;
    }
    .error-status {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class Neo4jHockeyDatabase:
    """Direct Neo4j database connection for hockey statistics"""
    
    def __init__(self):
        """Initialize Neo4j connection"""
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USERNAME', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', '')
        
        self.driver = None
        self.connected = False
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            self.connected = True
        except Exception as e:
            st.error(f"❌ Could not connect to Neo4j database: {e}")
            st.info("🔧 Check your .env file with correct NEO4J_URI, NEO4J_USER and NEO4J_PASSWORD")
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
    
    def execute_query(self, query, parameters=None):
        """Execute a Cypher query and return results"""
        if not self.connected:
            return []
        
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            st.error(f"Database error: {e}")
            return []
    
    @st.cache_data(ttl=600)
    def get_competitions(_self):
        """Get available competitions from database"""
        query = "MATCH (c:Competition) RETURN c.name AS competition ORDER BY c.name"
        results = _self.execute_query(query)
        return [record['competition'] for record in results] if results else ["SHL"]
    
    @st.cache_data(ttl=600)
    def get_seasons(_self):
        """Get available seasons from database"""
        query = "MATCH (s:Season) RETURN s.name AS season ORDER BY s.name DESC"
        results = _self.execute_query(query)
        return [record['season'] for record in results] if results else ["2024/2025", "2023/2024"]
    
    @st.cache_data(ttl=600)
    def get_teams(_self):
        """Get all teams from database"""
        query = """
        MATCH (t:Team) 
        RETURN t.name AS name, t.shortName AS shortName 
        ORDER BY t.name
        """
        results = _self.execute_query(query)
        return results if results else [
            {"name": "Frölunda HC", "shortName": "FHC"},
            {"name": "Skellefteå AIK", "shortName": "SKE"}
        ]
    
    @st.cache_data(ttl=300)
    def get_standings(_self, competition, season):
        """Get current standings for competition and season"""
        query = """
        MATCH (t:Team)-[rel:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        RETURN t.name AS team,
               count(g) AS games,
               sum(rel.win) AS wins,
               sum(rel.lost) AS losses,
               sum(rel.draw) AS draws,
               sum(rel.goalsFor) AS goals_for,
               sum(rel.goalsAgainst) AS goals_against,
               sum(rel.points) AS points
        ORDER BY points DESC, goals_for DESC
        """
        results = _self.execute_query(query, {"season": season, "competition": competition})
        return results if results else []
    
    @st.cache_data(ttl=300)
    def get_top_scorers(_self, competition, season, limit=10):
        """Get top goal scorers"""
        query = """
        MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        MATCH (p)-[:PLAYS_FOR]->(t:Team)
        RETURN p.firstName + ' ' + p.lastName AS player, 
               t.name AS team, 
               count(g) AS goals,
               count(DISTINCT game) AS games
        ORDER BY goals DESC, games ASC
        LIMIT $limit
        """
        results = _self.execute_query(query, {"season": season, "competition": competition, "limit": limit})
        return results if results else []
    
    @st.cache_data(ttl=300)
    def get_top_assists(_self, competition, season, limit=10):
        """Get top assist providers"""
        query = """
        MATCH (p:Player)-[:ASSISTED_IN]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        MATCH (p)-[:PLAYS_FOR]->(t:Team)
        RETURN p.firstName + ' ' + p.lastName AS player, 
               t.name AS team, 
               count(g) AS assists,
               count(DISTINCT game) AS games
        ORDER BY assists DESC, games ASC
        LIMIT $limit
        """
        results = _self.execute_query(query, {"season": season, "competition": competition, "limit": limit})
        return results if results else []
    
    @st.cache_data(ttl=300)
    def get_penalty_leaders(_self, competition, season, limit=10):
        """Get most penalized players"""
        query = """
        MATCH (p:Player)-[:COMMITTED]->(pen:Penalty)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        MATCH (p)-[:PLAYS_FOR]->(t:Team)
        RETURN p.firstName + ' ' + p.lastName AS player, 
               t.name AS team, 
               count(pen) AS penalties,
               sum(pen.minutes) AS penalty_minutes,
               count(DISTINCT game) AS games
        ORDER BY penalties DESC, penalty_minutes DESC
        LIMIT $limit
        """
        results = _self.execute_query(query, {"season": season, "competition": competition, "limit": limit})
        return results if results else []
    
    @st.cache_data(ttl=300)
    def get_recent_games(_self, competition, season, limit=15):
        """Get recent games"""
        query = """
        MATCH (g:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        RETURN g.date AS date, 
               g.homeTeam AS home_team, 
               g.awayTeam AS away_team, 
               g.score AS score,
               g.spectators AS spectators,
               g.title AS title
        ORDER BY g.date DESC
        LIMIT $limit
        """
        results = _self.execute_query(query, {"season": season, "competition": competition, "limit": limit})
        return results if results else []
    
    @st.cache_data(ttl=300)
    def get_team_stats(_self, team_name, competition, season):
        """Get detailed team statistics"""
        query = """
        MATCH (t:Team {name: $team_name})-[rel:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {name: $season})
        MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
        RETURN count(g) AS games,
               sum(CASE WHEN rel.result = 'W' THEN 1 ELSE 0 END) AS wins,
               sum(CASE WHEN rel.result = 'L' THEN 1 ELSE 0 END) AS losses,
               sum(rel.goalsFor) AS goals_for,
               sum(rel.goalsAgainst) AS goals_against,
               sum(rel.points) AS points,
               avg(rel.goalsFor) AS avg_goals_for,
               avg(rel.goalsAgainst) AS avg_goals_against
        """
        results = _self.execute_query(query, {"team_name": team_name, "season": season, "competition": competition})
        return results[0] if results else {}
    
    def get_database_info(self):
        """Get general database information"""
        queries = {
            "teams": "MATCH (t:Team) RETURN count(t) AS count",
            "players": "MATCH (p:Player) RETURN count(p) AS count",
            "games": "MATCH (g:Game) RETURN count(g) AS count",
            "goals": "MATCH (goal:Goal) RETURN count(goal) AS count",
            "penalties": "MATCH (pen:Penalty) RETURN count(pen) AS count"
        }
        
        info = {}
        for key, query in queries.items():
            result = self.execute_query(query)
            info[key] = result[0]['count'] if result else 0
        
        return info

def main():
    """Main application function"""
    
    # Initialize database connection
    db = Neo4jHockeyDatabase()
    
    # Header
    st.markdown('<h1 class="main-header">🏒 SHL Hockey Statistics - Live Neo4j Data</h1>', unsafe_allow_html=True)
    
    # Connection status
    if db.connected:
        st.markdown('<div class="connection-status">🔗 Connected to Neo4j database</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-status">❌ No database connection</div>', unsafe_allow_html=True)
        st.stop()
    
    # Sidebar for filters
    st.sidebar.header("🔧 Filters")
    
    # Get data for filters
    competitions = db.get_competitions()
    seasons = db.get_seasons()
    teams = db.get_teams()
    
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
    db_info = db.get_database_info()
    if db_info:
        st.sidebar.markdown(f"🏒 {db_info.get('teams', 0)} teams")
        st.sidebar.markdown(f"👤 {db_info.get('players', 0)} players")
        st.sidebar.markdown(f"🎮 {db_info.get('games', 0)} games")
        st.sidebar.markdown(f"⚽ {db_info.get('goals', 0)} goals")
        st.sidebar.markdown(f"⚠️ {db_info.get('penalties', 0)} penalties")
    
    # Cache controls
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Update cache"):
        st.cache_data.clear()
        st.success("Cache updated!")
        st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏆 Teams", "👤 Players", "🏒 Games"])
    
    with tab1:
        show_dashboard(db, selected_competition, selected_season)
    
    with tab2:
        show_teams(db, selected_competition, selected_season, teams)
    
    with tab3:
        show_players(db, selected_competition, selected_season)
    
    with tab4:
        show_games(db, selected_competition, selected_season)
    
    # Clean up
    db.close()

def show_dashboard(db, competition, season):
    """Display main dashboard with live data"""
    st.header(f"📊 {competition} {season} Dashboard")
    
    # Get standings for calculations
    standings = db.get_standings(competition, season)
    
    if standings:
        df = pd.DataFrame(standings)
        
        # Calculate metrics
        total_teams = len(df)
        total_games = df['games'].sum()
        total_goals = df['goals_for'].sum()
        avg_goals_per_game = total_goals / total_games if total_games > 0 else 0
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏒 Teams", total_teams)
        
        with col2:
            st.metric("🎮 Total games", f"{total_games:,}")
        
        with col3:
            st.metric("⚽ Total goals", f"{total_goals:,}")
        
        with col4:
            st.metric("📈 Avg goals/game", f"{avg_goals_per_game:.2f}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥅 Top scoring teams")
            top_teams = df.head(6)
            fig = px.bar(
                x=top_teams['goals_for'],
                y=top_teams['team'],
                orientation='h',
                title="Goals scored this season",
                labels={'x': 'Goals', 'y': 'Team'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Standings (top 6)")
            standings_table = top_teams[['team', 'points', 'wins', 'losses', 'goals_for', 'goals_against']]
            standings_table.columns = ['Team', 'Points', 'Wins', 'Losses', 'Goals For', 'Goals Against']
            st.dataframe(standings_table, use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ No data available for selected competition and season.")

def show_teams(db, competition, season, teams):
    """Display team statistics"""
    st.header(f"🏆 {competition} {season} Team Statistics")
    
    # Team selector
    team_options = ["📊 All teams (Table)"] + [f"🏒 {team['name']}" for team in teams]
    selected_option = st.selectbox("Select view:", team_options)
    
    if selected_option == "📊 All teams (Table)":
        show_standings(db, competition, season)
    else:
        team_name = selected_option.replace("🏒 ", "")
        show_team_details(db, team_name, competition, season)

def show_standings(db, competition, season):
    """Display full standings table"""
    st.subheader("📊 Full standings")
    
    standings = db.get_standings(competition, season)
    
    if standings:
        df = pd.DataFrame(standings)
        
        # Add calculated columns
        df['position'] = range(1, len(df) + 1)
        df['goal_diff'] = df['goals_for'] - df['goals_against']
        df['points_per_game'] = (df['points'] / df['games']).round(2)
        df['win_percentage'] = (df['wins'] / df['games'] * 100).round(1)
        
        # Prepare display
        display_df = df[['position', 'team', 'games', 'wins', 'losses', 
                        'goals_for', 'goals_against', 'goal_diff', 'points', 
                        'points_per_game', 'win_percentage']].copy()
        
        display_df.columns = ['Pos', 'Team', 'GP', 'W', 'L', 'GF', 'GA', 'GD', 'P', 'P/GP', 'W%']
        
        # Style based on position
        def highlight_positions(row):
            if row['Pos'] <= 6:  # Playoff positions
                return ['background-color: #d4edda'] * len(row)
            elif row['Pos'] >= len(display_df) - 1:  # Bottom 2
                return ['background-color: #f8d7da'] * len(row)
            else:
                return [''] * len(row)
        
        # Apply styling without matplotlib dependency
        try:
            styled_df = display_df.style.apply(highlight_positions, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except:
            # Fallback without styling if matplotlib is not available
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # League insights
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🥇 League leaders")
            leader = df.iloc[0]
            st.markdown(f"**Most points:** {leader['team']} ({leader['points']} p)")
            
            best_offense = df.loc[df['goals_for'].idxmax()]
            st.markdown(f"**Best offense:** {best_offense['team']} ({best_offense['goals_for']} goals)")
            
            best_defense = df.loc[df['goals_against'].idxmin()]
            st.markdown(f"**Best defense:** {best_defense['team']} ({best_defense['goals_against']} allowed)")
        
        with col2:
            st.subheader("📊 Averages")
            st.markdown(f"**Avg points:** {df['points'].mean():.1f}")
            st.markdown(f"**Avg goals for:** {df['goals_for'].mean():.1f}")
            st.markdown(f"**Avg goals against:** {df['goals_against'].mean():.1f}")
        
        with col3:
            st.subheader("🎯 Interesting facts")
            if len(df) >= 2:
                gap = df.iloc[0]['points'] - df.iloc[1]['points']
                st.markdown(f"**Leader gap:** {gap} points")
                
                # Playoff line analysis
                if len(df) >= 6:
                    playoff_gap = df.iloc[5]['points'] - df.iloc[6]['points'] if len(df) > 6 else 0
                    st.markdown(f"**Playoff race:** {playoff_gap} points gap")
    
    else:
        st.error("❌ Could not load standings data")

def show_team_details(db, team_name, competition, season):
    """Display individual team details"""
    st.subheader(f"🏒 {team_name}")
    
    team_stats = db.get_team_stats(team_name, competition, season)
    
    if team_stats and team_stats.get('games', 0) > 0:
        # Calculate additional metrics
        goal_diff = team_stats['goals_for'] - team_stats['goals_against']
        ppg = team_stats['points'] / team_stats['games']
        win_pct = team_stats['wins'] / team_stats['games'] * 100
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Games played", team_stats['games'])
            st.metric("Wins", team_stats['wins'])
        
        with col2:
            st.metric("Losses", team_stats['losses'])
            st.metric("Points", team_stats['points'])
        
        with col3:
            st.metric("Goals for", team_stats['goals_for'])
            st.metric("Goals against", team_stats['goals_against'])
        
        with col4:
            st.metric("Goal difference", f"+{goal_diff}" if goal_diff >= 0 else str(goal_diff))
            st.metric("Points/game", f"{ppg:.2f}")
        
        # Performance charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Win/Loss distribution")
            fig = px.pie(
                values=[team_stats['wins'], team_stats['losses']],
                names=['Wins', 'Losses'],
                title="Match results"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚽ Goals comparison")
            fig = px.bar(
                x=['Goals for', 'Goals against'],
                y=[team_stats['goals_for'], team_stats['goals_against']],
                title="Offense vs Defense"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.error(f"❌ Could not load statistics for {team_name}")

def show_players(db, competition, season):
    """Display player statistics"""
    st.header(f"👤 {competition} {season} Player Statistics")
    
    # Player stats tabs
    tab1, tab2, tab3 = st.tabs(["🥅 Goal Scorers", "🎯 Assist Leaders", "⚠️ Penalties"])
    
    with tab1:
        show_player_goals(db, competition, season)
    
    with tab2:
        show_player_assists(db, competition, season)
    
    with tab3:
        show_player_penalties(db, competition, season)

def show_player_goals(db, competition, season):
    """Display top goal scorers"""
    st.subheader("🥅 Top goal scorers")
    
    limit = st.slider("Number of players to show:", 5, 50, 15)
    
    scorers = db.get_top_scorers(competition, season, limit)
    
    if scorers:
        df = pd.DataFrame(scorers)
        df['rank'] = range(1, len(df) + 1)
        df['goals_per_game'] = (df['goals'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'goals', 'games', 'goals_per_game']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Games', 'Goals/game']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Top 10 goal scorers")
            top_10 = df.head(10)
            fig = px.bar(
                x=top_10['goals'],
                y=top_10['player'],
                orientation='h',
                title="Goals this season",
                labels={'x': 'Goals', 'y': 'Player'}
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No goal scoring data available")

def show_player_assists(db, competition, season):
    """Display top assist providers"""
    st.subheader("🎯 Top assist leaders")
    
    limit = st.slider("Number of players to show:", 5, 50, 15, key="assists_limit")
    
    assists = db.get_top_assists(competition, season, limit)
    
    if assists:
        df = pd.DataFrame(assists)
        df['rank'] = range(1, len(df) + 1)
        df['assists_per_game'] = (df['assists'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'assists', 'games', 'assists_per_game']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Assists', 'Games', 'Assists/game']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Top 10 assist leaders")
            top_10 = df.head(10)
            fig = px.bar(
                x=top_10['assists'],
                y=top_10['player'],
                orientation='h',
                title="Assists this season",
                labels={'x': 'Assists', 'y': 'Player'}
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No assist data available")

def show_player_penalties(db, competition, season):
    """Display penalty leaders"""
    st.subheader("⚠️ Most penalized players")
    
    limit = st.slider("Number of players to show:", 5, 50, 15, key="penalty_limit")
    
    penalties = db.get_penalty_leaders(competition, season, limit)
    
    if penalties:
        df = pd.DataFrame(penalties)
        df['rank'] = range(1, len(df) + 1)
        df['penalties_per_game'] = (df['penalties'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'penalties', 'penalty_minutes', 'games', 'penalties_per_game']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Penalties', 'PIM', 'Games', 'PEN/game']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Top 10 most penalized")
            top_10 = df.head(10)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    x=top_10['penalties'],
                    y=top_10['player'],
                    orientation='h',
                    title="Number of penalties",
                    labels={'x': 'Penalties', 'y': 'Player'}
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    x=top_10['penalty_minutes'],
                    y=top_10['player'],
                    orientation='h',
                    title="Penalty minutes",
                    labels={'x': 'Minutes', 'y': 'Player'}
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No penalty data available")

def show_games(db, competition, season):
    """Display recent games"""
    st.header(f"🏒 {competition} {season} Games")
    
    limit = st.slider("Number of games to show:", 5, 50, 20)
    
    games = db.get_recent_games(competition, season, limit)
    
    if games:
        df = pd.DataFrame(games)
        
        # Format the display
        display_df = df[['date', 'home_team', 'away_team', 'score', 'spectators']].copy()
        display_df.columns = ['Date', 'Home Team', 'Away Team', 'Score', 'Attendance']
        
        # Format attendance
        if 'spectators' in df.columns:
            display_df['Attendance'] = display_df['Attendance'].apply(
                lambda x: f"{int(x):,}" if pd.notnull(x) and x != 0 else "N/A"
            )
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Game statistics
        if len(df) > 0:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Game statistics")
                total_games = len(df)
                st.metric("Games shown", total_games)
                
                if 'spectators' in df.columns:
                    valid_attendance = df['spectators'].dropna()
                    valid_attendance = valid_attendance[valid_attendance > 0]
                    if len(valid_attendance) > 0:
                        avg_attendance = valid_attendance.mean()
                        max_attendance = valid_attendance.max()
                        st.metric("Avg attendance", f"{avg_attendance:,.0f}")
                        st.metric("Highest attendance", f"{max_attendance:,}")
            
            with col2:
                st.subheader("⚽ Goal statistics")
                if 'score' in df.columns:
                    try:
                        # Parse scores to calculate goal statistics
                        scores = df['score'].str.split('-', expand=True)
                        if len(scores.columns) >= 2:
                            scores = scores.astype(int)
                            total_goals = scores.sum().sum()
                            avg_goals = total_goals / len(df)
                            highest_score = df.loc[scores.sum(axis=1).idxmax(), 'score']
                            
                            st.metric("Total goals", total_goals)
                            st.metric("Avg goals/game", f"{avg_goals:.1f}")
                            st.metric("Highest scoring game", highest_score)
                    except:
                        st.info("Could not analyze goal statistics")
    
    else:
        st.warning("⚠️ No game data available")

if __name__ == "__main__":
    main()
