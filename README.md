# 🏒 Streamlit Hockey Statistics Dashboard

A comprehensive Streamlit web application for displaying hockey statistics from a Neo4j database, featuring integration with MCP (Model Context Protocol) tools.

## 🌟 Features

### 📊 Dashboard Overview
- Key performance metrics and season statistics
- Top-performing teams visualization
- League-wide insights and trends

### 🏆 Teams & Standings
- Complete league standings with advanced metrics
- Individual team performance analysis
- Win/loss records and goal differentials
- Team comparison tools

### 👤 Player Statistics
- **Goal Scorers**: Top goal-scoring players across the league
- **Assist Leaders**: Players with most assists
- **Penalty Leaders**: Most penalized players with minutes

### 🏒 Games Analysis
- Recent game results with attendance figures
- Game statistics and scoring trends
- Attendance analysis and insights

## 🗃️ Database Integration

This application connects to a Neo4j hockey database with the following structure:

### Node Types
- **Player**: Individual hockey players with names and numbers
- **Team**: Hockey teams with names and short names
- **Game**: Individual games with scores, dates, and attendance
- **Goal**: Scoring events in games
- **Penalty**: Penalty events with descriptions and minutes
- **Season**: Competition seasons (e.g., "2023/2024", "2024/2025")
- **Competition**: Leagues/competitions (e.g., "SHL")

### Relationships
- `PLAYS_FOR`: Player → Team
- `SCORED`: Player → Goal
- `ASSISTED_IN`: Player → Goal
- `COMMITTED`: Player → Penalty
- `IN_GAME`: Goal/Penalty → Game
- `PLAYED`: Team → Game (with properties: result, goalsFor, goalsAgainst, points, home)
- `PART_OF`: Game/Competition → Season

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Access to Neo4j hockey database
- MCP tools configured for database access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tullanders/Streamlit-Hockey-Stats.git
   cd Streamlit-Hockey-Stats
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Basic version (with sample data)
   streamlit run app_basic.py
   
   # Neo4j integrated version (requires MCP setup)
   streamlit run app_neo4j.py
   
   # Full-featured version (requires plotly)
   streamlit run app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📁 File Structure

```
Streamlit-Hockey-Stats/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app.py                   # Full-featured app with Plotly charts
├── app_basic.py             # Basic version with built-in Streamlit charts
├── app_neo4j.py             # Neo4j integrated version with MCP tools
└── .env                     # Environment variables (not in repo)
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for any database configuration:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
MCP_SERVER_URL=your_mcp_server_url
```

### Database Queries
The application uses Cypher queries through MCP tools:

```cypher
# Top goal scorers
MATCH (p:Player)-[:SCORED]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
MATCH (p)-[:PLAYS_FOR]->(t:Team)
RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS goals
ORDER BY goals DESC LIMIT $limit

# Team standings
MATCH (t:Team)-[rel:PLAYED]->(g:Game)-[:PART_OF]->(s:Season {name: $season})
MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
RETURN t.name AS team,
       count(g) AS games,
       sum(CASE WHEN rel.result = 'W' THEN 1 ELSE 0 END) AS wins,
       sum(CASE WHEN rel.result = 'L' THEN 1 ELSE 0 END) AS losses,
       sum(rel.goalsFor) AS goals_for,
       sum(rel.goalsAgainst) AS goals_against,
       sum(rel.points) AS points
ORDER BY points DESC
```

## 🎨 User Interface

### Sidebar Filters
- **Competition Selection**: Choose from available competitions (e.g., SHL)
- **Season Selection**: Filter by specific seasons
- **Database Status**: Shows connection and data loading status

### Main Tabs
1. **📊 Dashboard**: Overview with key metrics and charts
2. **🏆 Teams**: Standings and individual team analysis
3. **👤 Players**: Player statistics across different categories
4. **🏒 Games**: Recent games and match analysis

### Interactive Features
- **Real-time Data**: Live updates from Neo4j database
- **Responsive Design**: Works on desktop and mobile devices
- **Data Export**: Download statistics as CSV files
- **Advanced Filtering**: Filter by teams, seasons, and date ranges

## 🛠️ Development

### Adding New Features

1. **New Statistics**: Add queries to the `Neo4jHockeyAPI` class
2. **New Visualizations**: Create functions in the main app file
3. **New Pages**: Add tabs in the main navigation

### Database Schema Extensions
To add new node types or relationships:

1. Update the `Neo4jHockeyAPI` class methods
2. Add corresponding Cypher queries
3. Update the UI components to display new data

## 📊 Sample Queries

### Get assist leaders:
```python
def get_player_assists(competition, season, limit=10):
    cypher_query = """
    MATCH (p:Player)-[:ASSISTED_IN]->(g:Goal)-[:IN_GAME]->(game:Game)-[:PART_OF]->(s:Season {name: $season})
    MATCH (s)-[:PART_OF]->(c:Competition {name: $competition})
    MATCH (p)-[:PLAYS_FOR]->(t:Team)
    RETURN p.firstName + ' ' + p.lastName AS player, t.name AS team, count(g) AS assists
    ORDER BY assists DESC LIMIT $limit
    """
    return mcp_hockey_neo4j_runcypher(cypher_query, {"season": season, "competition": competition, "limit": limit})
```

### Get team performance:
```python
def get_team_performance(team_name, competition, season):
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
    return mcp_hockey_neo4j_runcypher(cypher_query, {"team_name": team_name, "season": season, "competition": competition})
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Neo4j**: For the graph database technology
- **MCP Tools**: For database integration capabilities
- **SHL**: For the hockey data and statistics

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Contact the development team
- Check the documentation for troubleshooting

---

**Built with ❤️ for hockey fans and data enthusiasts!**