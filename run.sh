#!/bin/bash
# PowerScale CTO JSON Generator - Linux/Ubuntu Startup Script
# This script sets up and runs the Flask application on Linux systems

set -e  # Exit on error

echo "=============================================="
echo "PowerScale CTO JSON Generator"
echo "=============================================="
echo ""

# Check if Python is installed
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    PY_VERSION=$(python --version 2>&1 | grep -oP '\d+' | head -1)
    if [ "$PY_VERSION" = "3" ]; then
        PYTHON_CMD="python"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  RHEL/CentOS:  sudo yum install python3 python3-pip"
    exit 1
fi

# Check Python version (need 3.8+)
PY_FULL_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
PY_MAJOR=$(echo "$PY_FULL_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_FULL_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8 or higher is required (found $PY_FULL_VERSION)"
    exit 1
fi

echo "Using Python: $PYTHON_CMD (version $PY_FULL_VERSION)"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created successfully"
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "ERROR: Virtual environment activation script not found"
    exit 1
fi

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "Virtual environment activated: $VIRTUAL_ENV"

# Verify PSI database module exists
if [ ! -f "psi_database.py" ]; then
    echo "ERROR: psi_database.py not found. Please ensure you have the complete application package."
    exit 1
fi

# Verify PSI configs directory exists
if [ ! -d "psi_configs" ]; then
    echo "WARNING: psi_configs/ directory not found. PSI file browser will not work."
fi

# Install dependencies (explicitly using venv Python to avoid externally-managed-environment issues)
echo "Installing/updating dependencies..."
echo "Using Python: $VIRTUAL_ENV/bin/python3"
echo "Python version: $($VIRTUAL_ENV/bin/python3 --version)"
$VIRTUAL_ENV/bin/python3 -m pip install --upgrade pip -q
$VIRTUAL_ENV/bin/python3 -m pip install -r requirements.txt -q

# Get IP address for display
IP_ADDRESS=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")

# Count bundled files
COMPUTE_COUNT=$(ls psi_configs/infinity/compute/*.conf 2>/dev/null | wc -l)
SSD_COUNT=$(ls psi_configs/infinity/ssd/*.conf 2>/dev/null | wc -l)
NIC_COUNT=$(ls psi_configs/FE/*.conf 2>/dev/null | wc -l)
TOTAL_PSI=$((COMPUTE_COUNT + SSD_COUNT + NIC_COUNT))

# Run the application
echo ""
echo "=============================================="
echo "Starting PowerScale CTO JSON Generator..."
echo ""
echo "Local access:    http://localhost:5000"
echo "Network access:  http://$IP_ADDRESS:5000"
echo ""
if [ $TOTAL_PSI -gt 0 ]; then
    echo "Bundled PSI configs: $TOTAL_PSI files"
    echo "  - Compute: $COMPUTE_COUNT"
    echo "  - SSD: $SSD_COUNT"
    echo "  - NIC: $NIC_COUNT"
    echo ""
fi
echo "Documentation:   USER_MANUAL.md"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

# Use venv python explicitly to avoid system python issues
$VIRTUAL_ENV/bin/python3 -c "
from app import app
print('Flask application starting...')
app.run(host='0.0.0.0', port=5000, debug=False)
"
