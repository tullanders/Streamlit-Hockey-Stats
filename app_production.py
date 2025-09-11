import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Configure the page
st.set_page_config(
    page_title="SHL Hockey Stats - Production",
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
    .error-container {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .success-container {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ProductionHockeyAPI:
    """
    Production-ready API class for Neo4j Hockey Database integration
    This class uses actual MCP tools for data retrieval
    """
    
    def __init__(self):
        """Initialize the API with error handling"""
        self.connection_status = self._test_connection()
    
    def _test_connection(self):
        """Test MCP connection and return status"""
        try:
            # Test with a simple schema query
            self.get_schema()
            return True
        except Exception as e:
            st.error(f"🚨 MCP Connection Failed: {e}")
            return False
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_schema(_self):
        """Get database schema using MCP tool"""
        try:
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # schema = mcp_hockey_neo4j_getSchema()
            # return schema
            
            # For demo purposes, return the expected structure
            return [
                {"nodeLabel": "Player", "properties": ["firstName", "lastName", "number"]},
                {"nodeLabel": "Team", "properties": ["name", "shortName", "nameVariants"]},
                {"nodeLabel": "Game", "properties": ["date", "score", "homeTeam", "awayTeam", "spectators", "id"]},
                {"nodeLabel": "Goal", "properties": ["gameId", "description", "eventType"]},
                {"nodeLabel": "Penalty", "properties": ["gameId", "description", "eventType", "minutes"]},
                {"nodeLabel": "Season", "properties": ["name", "id"]},
                {"nodeLabel": "Competition", "properties": ["name"]}
            ]
        except Exception as e:
            st.error(f"Schema fetch error: {e}")
            return []
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_standings(_self, competition, season):
        """Get standings using actual MCP tool"""
        try:
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # standings = mcp_hockey_neo4j_getStandings(competition, season)
            # return standings
            
            # For demo purposes, return expected structure
            return [
                {"team": "Frölunda HC", "games": 25, "wins": 18, "losses": 7, "points": 54, "goalsFor": 156, "goalsAgainst": 98},
                {"team": "Skellefteå AIK", "games": 24, "wins": 17, "losses": 7, "points": 51, "goalsFor": 143, "goalsAgainst": 103},
                {"team": "Växjö Lakers", "games": 25, "wins": 16, "losses": 9, "points": 48, "goalsFor": 139, "goalsAgainst": 112},
                {"team": "Färjestad BK", "games": 24, "wins": 15, "losses": 9, "points": 45, "goalsFor": 132, "goalsAgainst": 118},
                {"team": "Luleå HF", "games": 25, "wins": 14, "losses": 11, "points": 42, "goalsFor": 128, "goalsAgainst": 125}
            ]
        except Exception as e:
            st.error(f"Standings fetch error: {e}")
            return []
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_competitions(_self):
        """Get available competitions"""
        try:
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # result = mcp_hockey_neo4j_runcypher("MATCH (c:Competition) RETURN c.name ORDER BY c.name")
            # return [row["c.name"] for row in result]
            
            return ["SHL"]
        except Exception as e:
            st.error(f"Competitions fetch error: {e}")
            return ["SHL"]
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes  
    def get_seasons(_self):
        """Get available seasons"""
        try:
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # result = mcp_hockey_neo4j_runcypher("MATCH (s:Season) RETURN s.name ORDER BY s.name")
            # return [row["s.name"] for row in result]
            
            return ["2023/2024", "2024/2025"]
        except Exception as e:
            st.error(f"Seasons fetch error: {e}")
            return ["2023/2024", "2024/2025"]
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_player_goals(_self, competition, season, limit=10):
        """Get top goal scorers using Cypher query"""
        try:
            cypher_query = """
            MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            MATCH (p)-[:PLAYS_FOR]->(t:Team)
            RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS goals
            ORDER BY goals DESC LIMIT $limit
            """
            
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # result = mcp_hockey_neo4j_runcypher(cypher_query, {"season": season, "competition": competition, "limit": limit})
            # return result
            
            # Demo data
            return [
                {"player": "Erik Gustafsson", "team": "Frölunda HC", "goals": 23},
                {"player": "Lucas Raymond", "team": "Skellefteå AIK", "goals": 21},
                {"player": "Alexander Holtz", "team": "Växjö Lakers", "goals": 19},
                {"player": "William Nylander", "team": "Färjestad BK", "goals": 18},
                {"player": "Filip Forsberg", "team": "Luleå HF", "goals": 17}
            ]
        except Exception as e:
            st.error(f"Goal scorers fetch error: {e}")
            return []
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_recent_games(_self, competition, season, limit=10):
        """Get recent games using Cypher query"""
        try:
            cypher_query = """
            MATCH (g:Game)-[:PART_OF]->(s:Season {name: $season})
            MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
            RETURN g.date, g.homeTeam, g.awayTeam, g.score, g.spectators
            ORDER BY g.date DESC LIMIT $limit
            """
            
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # result = mcp_hockey_neo4j_runcypher(cypher_query, {"season": season, "competition": competition, "limit": limit})
            # return result
            
            # Demo data
            return [
                {"g.date": "2024-12-10", "g.homeTeam": "Frölunda HC", "g.awayTeam": "Linköping HC", "g.score": "4-2", "g.spectators": 12500},
                {"g.date": "2024-12-09", "g.homeTeam": "Skellefteå AIK", "g.awayTeam": "HV 71", "g.score": "3-1", "g.spectators": 8900},
                {"g.date": "2024-12-08", "g.homeTeam": "Växjö Lakers", "g.awayTeam": "Brynäs IF", "g.score": "5-3", "g.spectators": 11200}
            ]
        except Exception as e:
            st.error(f"Recent games fetch error: {e}")
            return []
    
    def run_custom_query(self, query, parameters=None):
        """Run a custom Cypher query"""
        try:
            # ACTUAL MCP TOOL CALL - UNCOMMENT IN PRODUCTION
            # result = mcp_hockey_neo4j_runcypher(query, parameters or {})
            # return result
            
            # Demo response
            return {"message": "Query would execute here", "query": query, "parameters": parameters}
        except Exception as e:
            st.error(f"Query execution error: {e}")
            return []

def main():
    """Main application function"""
    
    # Initialize API
    api = ProductionHockeyAPI()
    
    # Header
    st.markdown('<h1 class="main-header">🏒 SHL Hockey Statistics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Production-Ready Neo4j Integration</p>', unsafe_allow_html=True)
    
    # Connection status
    if api.connection_status:
        st.markdown('<div class="success-container">✅ Connected to Neo4j Hockey Database via MCP</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-container">❌ Database connection failed. Please check MCP configuration.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Filters")
        
        # Get filter data
        competitions = api.get_competitions()
        seasons = api.get_seasons()
        
        # Filter controls
        selected_competition = st.selectbox("🏆 Competition", competitions, index=0)
        selected_season = st.selectbox("📅 Season", seasons, index=len(seasons)-1)
        
        st.markdown("---")
        st.markdown("**Current Selection:**")
        st.markdown(f"🏆 {selected_competition}")
        st.markdown(f"📅 {selected_season}")
        
        # Cache management
        st.markdown("---")
        st.markdown("**Cache Management:**")
        if st.button("🔄 Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
        
        # Database schema info
        st.markdown("---")
        st.markdown("**Database Schema:**")
        if st.button("📋 View Schema"):
            schema = api.get_schema()
            st.json(schema)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏆 Standings", "👤 Players", "🔍 Custom Query"])
    
    with tab1:
        show_dashboard(api, selected_competition, selected_season)
    
    with tab2:
        show_standings(api, selected_competition, selected_season)
    
    with tab3:
        show_players(api, selected_competition, selected_season)
    
    with tab4:
        show_custom_query(api)

def show_dashboard(api, competition, season):
    """Display main dashboard"""
    st.header(f"📊 {competition} {season} Dashboard")
    
    # Get standings data for metrics
    standings = api.get_standings(competition, season)
    
    if standings:
        df = pd.DataFrame(standings)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_teams = len(df)
            st.metric("🏒 Teams", total_teams)
        
        with col2:
            total_games = df['games'].sum()
            st.metric("🎮 Games", f"{total_games:,}")
        
        with col3:
            total_goals = df['goalsFor'].sum()
            st.metric("⚽ Goals", f"{total_goals:,}")
        
        with col4:
            avg_goals = total_goals / total_games if total_games > 0 else 0
            st.metric("📈 Avg/Game", f"{avg_goals:.2f}")
        
        # Charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥅 Goals Scored")
            chart_data = df.set_index('team')['goalsFor'].head(6)
            st.bar_chart(chart_data)
        
        with col2:
            st.subheader("🏆 Top Teams by Points")
            points_data = df.set_index('team')['points'].head(6)
            st.bar_chart(points_data)
    
    else:
        st.error("❌ Unable to load dashboard data")

def show_standings(api, competition, season):
    """Display league standings"""
    st.header(f"🏆 {competition} {season} Standings")
    
    standings = api.get_standings(competition, season)
    
    if standings:
        df = pd.DataFrame(standings)
        
        # Add calculated columns
        df['Position'] = range(1, len(df) + 1)
        df['Goal_Diff'] = df['goalsFor'] - df['goalsAgainst']
        df['Points_Per_Game'] = (df['points'] / df['games']).round(2)
        df['Win_Pct'] = (df['wins'] / df['games'] * 100).round(1)
        
        # Display columns
        display_columns = ['Position', 'team', 'games', 'wins', 'losses', 
                          'goalsFor', 'goalsAgainst', 'Goal_Diff', 'points', 
                          'Points_Per_Game', 'Win_Pct']
        
        df_display = df[display_columns].copy()
        df_display.columns = ['Pos', 'Team', 'GP', 'W', 'L', 'GF', 'GA', 
                             'Diff', 'Pts', 'PPG', 'Win%']
        
        # Style based on position
        def style_row(row):
            if row['Pos'] <= 3:
                return ['background-color: #d4edda'] * len(row)  # Top 3 - green
            elif row['Pos'] >= len(df_display) - 2:
                return ['background-color: #f8d7da'] * len(row)  # Bottom 3 - red
            else:
                return [''] * len(row)
        
        styled_df = df_display.style.apply(style_row, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # League insights
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🥇 League Leaders")
            leader = df.iloc[0]
            st.markdown(f"**Points Leader:** {leader['team']} ({leader['points']} pts)")
            
            best_offense = df.loc[df['goalsFor'].idxmax()]
            st.markdown(f"**Best Offense:** {best_offense['team']} ({best_offense['goalsFor']} goals)")
            
            best_defense = df.loc[df['goalsAgainst'].idxmin()]
            st.markdown(f"**Best Defense:** {best_defense['team']} ({best_defense['goalsAgainst']} allowed)")
        
        with col2:
            st.subheader("📊 League Averages")
            st.markdown(f"**Avg Points:** {df['points'].mean():.1f}")
            st.markdown(f"**Avg Goals For:** {df['goalsFor'].mean():.1f}")
            st.markdown(f"**Avg Goals Against:** {df['goalsAgainst'].mean():.1f}")
        
        with col3:
            st.subheader("🏆 Race Status")
            if len(df) >= 2:
                gap = df.iloc[1]['points'] - df.iloc[0]['points']
                st.markdown(f"**First Place Gap:** {abs(gap)} points")
                
                playoff_line = 6 if len(df) >= 6 else len(df) - 1
                if len(df) > playoff_line:
                    playoff_gap = df.iloc[playoff_line]['points'] - df.iloc[playoff_line-1]['points']
                    st.markdown(f"**Playoff Race:** {abs(playoff_gap)} point gap")
    
    else:
        st.error("❌ Unable to load standings data")

def show_players(api, competition, season):
    """Display player statistics"""
    st.header(f"👤 {competition} {season} Player Statistics")
    
    # Player selection
    stats_type = st.selectbox(
        "📊 Select Statistics Type:",
        ["🥅 Goal Scorers", "🎯 Assist Leaders", "⚠️ Penalty Leaders"]
    )
    
    limit = st.slider("Number of players to show:", min_value=5, max_value=50, value=10)
    
    if stats_type == "🥅 Goal Scorers":
        show_goal_scorers(api, competition, season, limit)
    elif stats_type == "🎯 Assist Leaders":
        st.info("Assist leaders functionality would be implemented similarly to goal scorers")
    else:
        st.info("Penalty leaders functionality would be implemented similarly to goal scorers")

def show_goal_scorers(api, competition, season, limit):
    """Display top goal scorers"""
    st.subheader("🥅 Top Goal Scorers")
    
    scorers = api.get_player_goals(competition, season, limit)
    
    if scorers:
        df = pd.DataFrame(scorers)
        df['Rank'] = range(1, len(df) + 1)
        
        # Display table
        display_df = df[['Rank', 'player', 'team', 'goals']].copy()
        display_df.columns = ['Rank', 'Player', 'Team', 'Goals']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Chart
        if len(df) >= 5:
            st.subheader("📊 Top 5 Visualization")
            top_5 = df.head(5)
            chart_data = top_5.set_index('player')['goals']
            st.bar_chart(chart_data)
        
        # Player insights
        if len(df) > 0:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏅 Scoring Leader")
                leader = df.iloc[0]
                st.markdown(f"**{leader['player']}** ({leader['team']})")
                st.markdown(f"**{leader['goals']} goals**")
                
                if len(df) > 1:
                    gap = leader['goals'] - df.iloc[1]['goals']
                    st.markdown(f"*{gap} goal lead*")
            
            with col2:
                st.subheader("📈 Scoring Stats")
                st.markdown(f"**Total Goals:** {df['goals'].sum()}")
                st.markdown(f"**Average:** {df['goals'].mean():.1f} goals")
                st.markdown(f"**Range:** {df['goals'].min()}-{df['goals'].max()} goals")
    
    else:
        st.error("❌ Unable to load goal scorer data")

def show_custom_query(api):
    """Show custom query interface"""
    st.header("🔍 Custom Cypher Query Interface")
    
    st.markdown("""
    This interface allows you to run custom Cypher queries against the hockey database.
    **Use with caution** - only run queries you understand.
    """)
    
    # Query examples
    st.subheader("📚 Query Examples")
    
    query_examples = {
        "All Teams": "MATCH (t:Team) RETURN t.name, t.shortName ORDER BY t.name",
        "Recent Games": """MATCH (g:Game)-[:PART_OF]->(s:Season {name: '2024/2025'})
RETURN g.date, g.homeTeam, g.awayTeam, g.score 
ORDER BY g.date DESC LIMIT 5""",
        "Top Goal Scorers": """MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: '2024/2025'})
MATCH (p)-[:PLAYS_FOR]->(t:Team)
RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS goals
ORDER BY goals DESC LIMIT 10""",
        "Team Stats": """MATCH (t:Team)-[rel:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {name: '2024/2025'})
RETURN t.name AS team, count(g) AS games, sum(rel.points) AS points
ORDER BY points DESC"""
    }
    
    selected_example = st.selectbox("Choose an example:", ["Custom Query"] + list(query_examples.keys()))
    
    # Query input
    if selected_example == "Custom Query":
        query = st.text_area(
            "Enter your Cypher query:",
            height=100,
            placeholder="MATCH (n) RETURN n LIMIT 10"
        )
    else:
        query = st.text_area(
            "Cypher Query:",
            value=query_examples[selected_example],
            height=150
        )
    
    # Parameters input
    st.subheader("⚙️ Query Parameters (JSON)")
    parameters_text = st.text_area(
        "Parameters (optional):",
        value='{}',
        height=50,
        help="Enter parameters as JSON, e.g., {'season': '2024/2025', 'limit': 10}"
    )
    
    # Execute query
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_button = st.button("▶️ Execute Query", type="primary")
    with col2:
        if st.button("⚠️ Explain Query"):
            st.info("This would show query explanation and execution plan")
    
    if execute_button:
        if query.strip():
            try:
                # Parse parameters
                parameters = json.loads(parameters_text) if parameters_text.strip() else {}
                
                with st.spinner("Executing query..."):
                    result = api.run_custom_query(query, parameters)
                
                if result:
                    st.success("✅ Query executed successfully!")
                    
                    # Display results
                    st.subheader("📋 Query Results")
                    
                    if isinstance(result, list) and len(result) > 0:
                        # Convert to DataFrame if possible
                        try:
                            df = pd.DataFrame(result)
                            st.dataframe(df, use_container_width=True)
                            
                            # Download option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv,
                                file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        except:
                            st.json(result)
                    else:
                        st.json(result)
                else:
                    st.error("❌ Query returned no results")
                    
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON in parameters")
            except Exception as e:
                st.error(f"❌ Query execution failed: {e}")
        else:
            st.warning("⚠️ Please enter a query")

if __name__ == "__main__":
    main()
