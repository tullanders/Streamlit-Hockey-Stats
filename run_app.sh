#!/bin/bash

# SHL Hockey Stats - Streamlit Application Runner
# This script helps you run different versions of the hockey stats application

echo "🏒 SHL Hockey Statistics Dashboard"
echo "=================================="
echo ""

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Installing..."
    pip install streamlit
fi

echo "Select which version to run:"
echo ""
echo "1. 📊 Basic Version (app_basic.py) - Uses built-in Streamlit charts, no external dependencies"
echo "2. 🎨 Full Version (app.py) - Includes Plotly charts and advanced visualizations" 
echo "3. 🔗 Neo4j Version (app_neo4j.py) - Integrated with Neo4j database via MCP tools"
echo "4. 🚀 Production Version (app_production.py) - Production-ready with error handling"
echo "5. 🧪 MCP Demo (mcp_demo.py) - Demonstrates MCP tool integration"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting Basic Version..."
        streamlit run app_basic.py
        ;;
    2)
        echo "🚀 Starting Full Version..."
        echo "Installing dependencies..."
        pip install plotly
        streamlit run app.py
        ;;
    3)
        echo "🚀 Starting Neo4j Version..."
        streamlit run app_neo4j.py
        ;;
    4)
        echo "🚀 Starting Production Version..."
        streamlit run app_production.py
        ;;
    5)
        echo "🚀 Starting MCP Demo..."
        streamlit run mcp_demo.py
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
