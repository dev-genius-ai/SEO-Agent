#!/bin/bash

set -e

echo "=================================="
echo "SEO Agent Setup"
echo "=================================="
echo ""

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
    echo ""
else
    echo ".env file already exists"
    echo ""
fi

echo "Installing Python dependencies..."
pip install -r requirements.txt
echo ""

echo "Initializing database..."
python -c "from app.models.database import init_db; init_db(); print('Database initialized')"
echo ""

echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To start the server:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To run demo:"
echo "  ./scripts/demo.sh"
echo ""

