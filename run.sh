#!/bin/bash

# Haiti National Bank - Startup Script

echo "========================================="
echo "Haiti National Bank - Money Transfer System"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Check if database exists
if [ ! -f "haiti_bank.db" ]; then
    echo "Database not found. Initializing..."
    flask init-db
    echo ""
    echo "Would you like to create a demo admin user? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        flask seed-db
    fi
fi

echo ""
echo "========================================="
echo "Starting Haiti National Bank..."
echo "========================================="
echo ""
echo "Access the application at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
