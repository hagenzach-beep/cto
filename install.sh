#!/bin/bash
# PowerScale CTO JSON Generator - Ubuntu/Linux Installation Script
# This script installs all system dependencies and sets up the application

set -e  # Exit on error

echo "=============================================="
echo "PowerScale CTO JSON Generator - Installer"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Count PSI database entries for display
PSI_DATABASE_COUNT=3  # compute, ssd, nic

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo -e "${RED}ERROR: Cannot detect OS version${NC}"
    exit 1
fi

echo "Detected OS: $OS $VER"
echo ""

# Verify all required files are present
echo "Checking installation files..."
MISSING_FILES=()

if [ ! -f "app.py" ]; then
    MISSING_FILES+=("app.py")
fi

if [ ! -f "psi_database.py" ]; then
    MISSING_FILES+=("psi_database.py")
fi

if [ ! -f "requirements.txt" ]; then
    MISSING_FILES+=("requirements.txt")
fi

if [ ! -f "README.md" ]; then
    MISSING_FILES+=("README.md")
fi

if [ ! -f "USER_MANUAL.md" ]; then
    MISSING_FILES+=("USER_MANUAL.md")
fi

if [ ! -d "templates" ]; then
    MISSING_FILES+=("templates/ directory")
fi

if [ ! -d "psi_configs" ]; then
    MISSING_FILES+=("psi_configs/ directory (bundled PSI configuration files)")
fi

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo -e "${RED}ERROR: Missing required files:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please ensure you have the complete application package."
    exit 1
fi

echo -e "${GREEN}All required files present ✓${NC}"
echo ""

# Check if running as root (not recommended for pip installs)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}WARNING: Running as root. It's recommended to run as a regular user.${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Function to install on Ubuntu/Debian
install_ubuntu() {
    echo -e "${GREEN}Installing dependencies for Ubuntu/Debian...${NC}"
    
    # Update package list
    echo "Updating package list..."
    sudo apt-get update
    
    # Install Python 3 and required packages
    echo "Installing Python 3 and dependencies..."
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        curl \
        wget
    
    # Verify Python installation
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}ERROR: Python 3 installation failed${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    echo -e "${GREEN}Python $PYTHON_VERSION installed successfully${NC}"
}

# Function to install on RHEL/CentOS/Fedora
install_rhel() {
    echo -e "${GREEN}Installing dependencies for RHEL/CentOS/Fedora...${NC}"
    
    # Check if dnf or yum
    if command -v dnf &> /dev/null; then
        PKG_MGR="dnf"
    else
        PKG_MGR="yum"
    fi
    
    echo "Using package manager: $PKG_MGR"
    
    # Install Python 3 and required packages
    echo "Installing Python 3 and dependencies..."
    sudo $PKG_MGR install -y \
        python3 \
        python3-pip \
        python3-devel \
        gcc \
        curl \
        wget
    
    # Verify Python installation
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}ERROR: Python 3 installation failed${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    echo -e "${GREEN}Python $PYTHON_VERSION installed successfully${NC}"
}

# Install based on OS
case "$OS" in
    *"Ubuntu"*|*"Debian"*)
        install_ubuntu
        ;;
    *"Red Hat"*|*"CentOS"*|*"Fedora"*|*"Rocky"*|*"AlmaLinux"*)
        install_rhel
        ;;
    *)
        echo -e "${YELLOW}WARNING: Unsupported OS: $OS${NC}"
        echo "Attempting to continue with Python 3..."
        if ! command -v python3 &> /dev/null; then
            echo -e "${RED}ERROR: Python 3 is not installed${NC}"
            exit 1
        fi
        ;;
esac

# Check Python version (need 3.8+)
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
PY_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo -e "${RED}ERROR: Python 3.8 or higher is required (found $PYTHON_VERSION)${NC}"
    echo "Please upgrade Python and run this script again."
    exit 1
fi

echo ""
echo "Python version check passed: $PYTHON_VERSION"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    exit 1
fi

# Verify we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}ERROR: Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}Virtual environment activated: $VIRTUAL_ENV${NC}"

# Upgrade pip (using venv pip, not system pip)
echo "Upgrading pip in virtual environment..."
$VIRTUAL_ENV/bin/python3 -m pip install --upgrade pip -q

# Install Python dependencies using venv pip
echo "Installing Python packages in virtual environment..."
$VIRTUAL_ENV/bin/python3 -m pip install -r requirements.txt

echo ""
echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo ""
echo "Installed components:"
echo "  ✓ Flask web application"
echo "  ✓ PSI Database module ($PSI_DATABASE_COUNT categories)"
echo "  ✓ Bundled PSI configuration files"
echo "    - Compute: $(ls psi_configs/infinity/compute/*.conf 2>/dev/null | wc -l) files"
echo "    - SSD: $(ls psi_configs/infinity/ssd/*.conf 2>/dev/null | wc -l) files"
echo "    - NIC: $(ls psi_configs/FE/*.conf 2>/dev/null | wc -l) files"
echo "  ✓ HTML templates and UI"
echo "  ✓ Documentation (README.md, USER_MANUAL.md)"
echo ""
echo "To start the application, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "Features available:"
echo "  - CTO JSON Generator"
echo "  - PSI Code Browser & Validator"
echo "  - PSI Configuration Comparison"
echo "  - Bundled PSI File Browser & Download"
echo "  - Hardware Upgrade Package Generator"
echo ""
echo "For documentation, see: README.md"
echo ""
