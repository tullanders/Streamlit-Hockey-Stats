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

# Ladda miljövariabler från .env-filen
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
        self.user = os.getenv('NEO4J_USER', 'neo4j')
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
            st.error(f"❌ Kunde inte ansluta till Neo4j databas: {e}")
            st.info("🔧 Kontrollera din .env fil med rätt NEO4J_URI, NEO4J_USER och NEO4J_PASSWORD")
    
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
            st.error(f"Databasfel: {e}")
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
               sum(CASE WHEN rel.result = 'W' THEN 1 ELSE 0 END) AS wins,
               sum(CASE WHEN rel.result = 'L' THEN 1 ELSE 0 END) AS losses,
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
        st.markdown('<div class="connection-status">🔗 Ansluten till Neo4j databas</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-status">❌ Ingen databasanslutning</div>', unsafe_allow_html=True)
        st.stop()
    
    # Sidebar for filters
    st.sidebar.header("🔧 Filter")
    
    # Get data for filters
    competitions = db.get_competitions()
    seasons = db.get_seasons()
    teams = db.get_teams()
    
    # Filter controls
    selected_competition = st.sidebar.selectbox("Tävling", competitions, index=0)
    selected_season = st.sidebar.selectbox("Säsong", seasons, index=0)
    
    # Display current selection
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Aktuellt val:**")
    st.sidebar.markdown(f"🏆 {selected_competition}")
    st.sidebar.markdown(f"📅 {selected_season}")
    
    # Database info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Databasinfo:**")
    db_info = db.get_database_info()
    if db_info:
        st.sidebar.markdown(f"🏒 {db_info.get('teams', 0)} lag")
        st.sidebar.markdown(f"👤 {db_info.get('players', 0)} spelare")
        st.sidebar.markdown(f"🎮 {db_info.get('games', 0)} matcher")
        st.sidebar.markdown(f"⚽ {db_info.get('goals', 0)} mål")
        st.sidebar.markdown(f"⚠️ {db_info.get('penalties', 0)} utvisningar")
    
    # Cache controls
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Uppdatera cache"):
        st.cache_data.clear()
        st.success("Cache uppdaterad!")
        st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🏆 Lag", "👤 Spelare", "🏒 Matcher", "🔍 Frågor"])
    
    with tab1:
        show_dashboard(db, selected_competition, selected_season)
    
    with tab2:
        show_teams(db, selected_competition, selected_season, teams)
    
    with tab3:
        show_players(db, selected_competition, selected_season)
    
    with tab4:
        show_games(db, selected_competition, selected_season)
    
    with tab5:
        show_custom_queries(db, selected_competition, selected_season)
    
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
            st.metric("🏒 Lag", total_teams)
        
        with col2:
            st.metric("🎮 Totalt matcher", f"{total_games:,}")
        
        with col3:
            st.metric("⚽ Totalt mål", f"{total_goals:,}")
        
        with col4:
            st.metric("📈 Snitt mål/match", f"{avg_goals_per_game:.2f}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥅 Bästa målskyttelagen")
            top_teams = df.head(6)
            fig = px.bar(
                x=top_teams['goals_for'],
                y=top_teams['team'],
                orientation='h',
                title="Mål gjorda denna säsong",
                labels={'x': 'Mål', 'y': 'Lag'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Poängtabell (topp 6)")
            standings_table = top_teams[['team', 'points', 'wins', 'losses', 'goals_for', 'goals_against']]
            standings_table.columns = ['Lag', 'Poäng', 'Vinster', 'Förluster', 'Mål för', 'Mål emot']
            st.dataframe(standings_table, use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ Ingen data tillgänglig för valda tävling och säsong.")

def show_teams(db, competition, season, teams):
    """Display team statistics"""
    st.header(f"🏆 {competition} {season} Lagstatistik")
    
    # Team selector
    team_options = ["📊 Alla lag (Tabell)"] + [f"🏒 {team['name']}" for team in teams]
    selected_option = st.selectbox("Välj vy:", team_options)
    
    if selected_option == "📊 Alla lag (Tabell)":
        show_standings(db, competition, season)
    else:
        team_name = selected_option.replace("🏒 ", "")
        show_team_details(db, team_name, competition, season)

def show_standings(db, competition, season):
    """Display full standings table"""
    st.subheader("📊 Fullständig tabell")
    
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
        
        display_df.columns = ['Pos', 'Lag', 'M', 'V', 'F', 'GM', 'IM', 'MS', 'P', 'P/M', 'V%']
        
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
            st.subheader("🥇 Ligaledare")
            leader = df.iloc[0]
            st.markdown(f"**Flest poäng:** {leader['team']} ({leader['points']} p)")
            
            best_offense = df.loc[df['goals_for'].idxmax()]
            st.markdown(f"**Bästa anfall:** {best_offense['team']} ({best_offense['goals_for']} mål)")
            
            best_defense = df.loc[df['goals_against'].idxmin()]
            st.markdown(f"**Bästa försvar:** {best_defense['team']} ({best_defense['goals_against']} insläppta)")
        
        with col2:
            st.subheader("📊 Genomsnitt")
            st.markdown(f"**Snitt poäng:** {df['points'].mean():.1f}")
            st.markdown(f"**Snitt mål för:** {df['goals_for'].mean():.1f}")
            st.markdown(f"**Snitt mål emot:** {df['goals_against'].mean():.1f}")
        
        with col3:
            st.subheader("🎯 Spännande fakta")
            if len(df) >= 2:
                gap = df.iloc[0]['points'] - df.iloc[1]['points']
                st.markdown(f"**Ledargap:** {gap} poäng")
                
                # Playoff line analysis
                if len(df) >= 6:
                    playoff_gap = df.iloc[5]['points'] - df.iloc[6]['points'] if len(df) > 6 else 0
                    st.markdown(f"**Slutspelsstrid:** {playoff_gap} poäng gap")
    
    else:
        st.error("❌ Kunde inte ladda tabelldata")

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
            st.metric("Spelade matcher", team_stats['games'])
            st.metric("Vinster", team_stats['wins'])
        
        with col2:
            st.metric("Förluster", team_stats['losses'])
            st.metric("Poäng", team_stats['points'])
        
        with col3:
            st.metric("Mål för", team_stats['goals_for'])
            st.metric("Mål emot", team_stats['goals_against'])
        
        with col4:
            st.metric("Målskillnad", f"+{goal_diff}" if goal_diff >= 0 else str(goal_diff))
            st.metric("Poäng/match", f"{ppg:.2f}")
        
        # Performance charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Vinst/Förlust fördelning")
            fig = px.pie(
                values=[team_stats['wins'], team_stats['losses']],
                names=['Vinster', 'Förluster'],
                title="Matchresultat"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚽ Mål jämförelse")
            fig = px.bar(
                x=['Mål för', 'Mål emot'],
                y=[team_stats['goals_for'], team_stats['goals_against']],
                title="Offensiv vs Defensiv"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.error(f"❌ Kunde inte ladda statistik för {team_name}")

def show_players(db, competition, season):
    """Display player statistics"""
    st.header(f"👤 {competition} {season} Spelarstatistik")
    
    # Player stats tabs
    tab1, tab2, tab3 = st.tabs(["🥅 Målskyttar", "🎯 Passningsgivare", "⚠️ Utvisningar"])
    
    with tab1:
        show_player_goals(db, competition, season)
    
    with tab2:
        show_player_assists(db, competition, season)
    
    with tab3:
        show_player_penalties(db, competition, season)

def show_player_goals(db, competition, season):
    """Display top goal scorers"""
    st.subheader("🥅 Bästa målskyttarna")
    
    limit = st.slider("Antal spelare att visa:", 5, 50, 15)
    
    scorers = db.get_top_scorers(competition, season, limit)
    
    if scorers:
        df = pd.DataFrame(scorers)
        df['rank'] = range(1, len(df) + 1)
        df['goals_per_game'] = (df['goals'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'goals', 'games', 'goals_per_game']].copy()
        display_df.columns = ['Rank', 'Spelare', 'Lag', 'Mål', 'Matcher', 'Mål/match']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Topp 10 målskyttar")
            top_10 = df.head(10)
            fig = px.bar(
                x=top_10['goals'],
                y=top_10['player'],
                orientation='h',
                title="Mål denna säsong",
                labels={'x': 'Mål', 'y': 'Spelare'}
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ Ingen målskytte-data tillgänglig")

def show_player_assists(db, competition, season):
    """Display top assist providers"""
    st.subheader("🎯 Bästa passningsgivarna")
    
    limit = st.slider("Antal spelare att visa:", 5, 50, 15, key="assists_limit")
    
    assists = db.get_top_assists(competition, season, limit)
    
    if assists:
        df = pd.DataFrame(assists)
        df['rank'] = range(1, len(df) + 1)
        df['assists_per_game'] = (df['assists'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'assists', 'games', 'assists_per_game']].copy()
        display_df.columns = ['Rank', 'Spelare', 'Lag', 'Assist', 'Matcher', 'Assist/match']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Topp 10 passningsgivare")
            top_10 = df.head(10)
            fig = px.bar(
                x=top_10['assists'],
                y=top_10['player'],
                orientation='h',
                title="Assists denna säsong",
                labels={'x': 'Assists', 'y': 'Spelare'}
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ Ingen assist-data tillgänglig")

def show_player_penalties(db, competition, season):
    """Display penalty leaders"""
    st.subheader("⚠️ Mest utvisade spelarna")
    
    limit = st.slider("Antal spelare att visa:", 5, 50, 15, key="penalty_limit")
    
    penalties = db.get_penalty_leaders(competition, season, limit)
    
    if penalties:
        df = pd.DataFrame(penalties)
        df['rank'] = range(1, len(df) + 1)
        df['penalties_per_game'] = (df['penalties'] / df['games']).round(2)
        
        # Display table
        display_df = df[['rank', 'player', 'team', 'penalties', 'penalty_minutes', 'games', 'penalties_per_game']].copy()
        display_df.columns = ['Rank', 'Spelare', 'Lag', 'Utvisningar', 'Utv.min', 'Matcher', 'Utv/match']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Top 10 chart
        if len(df) >= 5:
            st.subheader("📊 Topp 10 mest utvisade")
            top_10 = df.head(10)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    x=top_10['penalties'],
                    y=top_10['player'],
                    orientation='h',
                    title="Antal utvisningar",
                    labels={'x': 'Utvisningar', 'y': 'Spelare'}
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    x=top_10['penalty_minutes'],
                    y=top_10['player'],
                    orientation='h',
                    title="Utvisningsminuter",
                    labels={'x': 'Minuter', 'y': 'Spelare'}
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ Ingen utvisnings-data tillgänglig")

def show_games(db, competition, season):
    """Display recent games"""
    st.header(f"🏒 {competition} {season} Matcher")
    
    limit = st.slider("Antal matcher att visa:", 5, 50, 20)
    
    games = db.get_recent_games(competition, season, limit)
    
    if games:
        df = pd.DataFrame(games)
        
        # Format the display
        display_df = df[['date', 'home_team', 'away_team', 'score', 'spectators']].copy()
        display_df.columns = ['Datum', 'Hemmalag', 'Bortalag', 'Resultat', 'Åskådare']
        
        # Format attendance
        if 'spectators' in df.columns:
            display_df['Åskådare'] = display_df['Åskådare'].apply(
                lambda x: f"{int(x):,}" if pd.notnull(x) and x != 0 else "N/A"
            )
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Game statistics
        if len(df) > 0:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Matchstatistik")
                total_games = len(df)
                st.metric("Visade matcher", total_games)
                
                if 'spectators' in df.columns:
                    valid_attendance = df['spectators'].dropna()
                    valid_attendance = valid_attendance[valid_attendance > 0]
                    if len(valid_attendance) > 0:
                        avg_attendance = valid_attendance.mean()
                        max_attendance = valid_attendance.max()
                        st.metric("Snitt åskådare", f"{avg_attendance:,.0f}")
                        st.metric("Högsta åskådarantal", f"{max_attendance:,}")
            
            with col2:
                st.subheader("⚽ Målstatistik")
                if 'score' in df.columns:
                    try:
                        # Parse scores to calculate goal statistics
                        scores = df['score'].str.split('-', expand=True)
                        if len(scores.columns) >= 2:
                            scores = scores.astype(int)
                            total_goals = scores.sum().sum()
                            avg_goals = total_goals / len(df)
                            highest_score = df.loc[scores.sum(axis=1).idxmax(), 'score']
                            
                            st.metric("Totalt mål", total_goals)
                            st.metric("Snitt mål/match", f"{avg_goals:.1f}")
                            st.metric("Högst målmatch", highest_score)
                    except:
                        st.info("Kunde inte analysera målstatistik")
    
    else:
        st.warning("⚠️ Ingen matchdata tillgänglig")

def show_custom_queries(db, competition, season):
    """Custom query interface"""
    st.header("🔍 Anpassade databasfrågor")
    
    st.markdown("""
    Här kan du köra egna Cypher-frågor mot hockeydatabasen.
    **Använd med försiktighet** - kör bara frågor du förstår.
    """)
    
    # Query examples
    st.subheader("📚 Exempel på frågor")
    
    examples = {
        "Alla lag": "MATCH (t:Team) RETURN t.name, t.shortName ORDER BY t.name",
        "Senaste matcher": f"""MATCH (g:Game)-[:PART_OF]->(s:Season {{name: '{season}'}})
RETURN g.date, g.homeTeam, g.awayTeam, g.score 
ORDER BY g.date DESC LIMIT 10""",
        "Målskyttar för specifikt lag": f"""MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {{name: '{season}'}})
MATCH (p)-[:PLAYS_FOR]->(t:Team {{name: 'Frölunda HC'}})
RETURN p.firstName + ' ' + p.lastName AS spelare, count(g) AS mål
ORDER BY mål DESC""",
        "Matcher för specifikt lag": f"""MATCH (t:Team {{name: 'Frölunda HC'}})-[:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {{name: '{season}'}})
RETURN g.date, g.homeTeam, g.awayTeam, g.score
ORDER BY g.date DESC LIMIT 10"""
    }
    
    selected_example = st.selectbox("Välj exempel:", ["Egen fråga"] + list(examples.keys()))
    
    # Query input
    if selected_example == "Egen fråga":
        query = st.text_area(
            "Skriv din Cypher-fråga:",
            height=100,
            placeholder="MATCH (n) RETURN n LIMIT 10"
        )
    else:
        query = st.text_area(
            "Cypher-fråga:",
            value=examples[selected_example],
            height=150
        )
    
    # Execute query
    col1, col2 = st.columns([1, 3])
    with col1:
        execute_button = st.button("▶️ Kör fråga", type="primary")
    
    if execute_button and query.strip():
        with st.spinner("Kör fråga..."):
            try:
                results = db.execute_query(query)
                
                if results:
                    st.success(f"✅ Fråga lyckades! Returnerade {len(results)} rader.")
                    
                    # Display results
                    st.subheader("📋 Resultat")
                    
                    # Convert to DataFrame if possible
                    try:
                        df = pd.DataFrame(results)
                        st.dataframe(df, use_container_width=True)
                        
                        # Download option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Ladda ner som CSV",
                            data=csv,
                            file_name=f"hockey_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        # If DataFrame conversion fails, show as JSON
                        st.json(results)
                        st.info(f"Kunde inte konvertera till tabell: {e}")
                
                else:
                    st.warning("⚠️ Frågan returnerade inga resultat")
                    
            except Exception as e:
                st.error(f"❌ Fel vid körning av fråga: {e}")
    
    elif execute_button:
        st.warning("⚠️ Skriv en fråga först")

if __name__ == "__main__":
    main()
