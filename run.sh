#!/bin/bash

# Haiti Banking System 2.0 - Start Script

echo "Starting Haiti Banking System 2.0..."
echo "===================================="

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
pip install -r requirements.txt

# Check if database exists
if [ ! -f "haiti_bank.db" ]; then
    echo "Database not found. Initializing..."
    python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
    echo ""
    echo "Would you like to seed the database with sample data? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        flask seed-db
    fi
fi

echo ""
echo "Starting application..."
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
