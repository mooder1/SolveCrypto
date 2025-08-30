#!/bin/bash

# SolveCrypto v2.0 Installation Script

echo "=============================================="
echo "        SolveCrypto v2.0 Installation"
echo "=============================================="

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✓ Python $PYTHON_VERSION is supported"
else
    echo "✗ Python $PYTHON_VERSION is not supported. Please upgrade to Python 3.8 or higher"
    exit 1
fi

# Check if pip is installed
echo "Checking pip installation..."
if command -v pip &> /dev/null; then
    echo "✓ pip is installed"
else
    echo "✗ pip is not installed. Please install pip first"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Create output directory
echo "Creating output directory..."
mkdir -p Output
chmod 755 Output
echo "✓ Output directory created"

# Set executable permissions
echo "Setting executable permissions..."
chmod +x main.py
chmod +x test_solver.py
echo "✓ Executable permissions set"

# Run basic tests
echo "Running basic tests..."
if python3 -c "import main, solver, MoodRSA, config, utils; print('All modules imported successfully')"; then
    echo "✓ All modules imported successfully"
else
    echo "✗ Module import test failed"
    exit 1
fi

# Optional: Run full test suite
echo ""
read -p "Do you want to run the full test suite? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running test suite..."
    python3 test_solver.py
fi

echo ""
echo "=============================================="
echo "     SolveCrypto v2.0 Installation Complete!"
echo "=============================================="
echo ""
echo "Usage:"
echo "  python3 main.py                 # Start the application"
echo "  python3 main.py --help          # Show help"
echo "  python3 main.py --version       # Show version"
echo "  python3 main.py --debug         # Enable debug mode"
echo "  python3 test_solver.py          # Run tests"
echo ""
echo "For more information, see README.md"
echo ""