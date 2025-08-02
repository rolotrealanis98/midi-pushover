#!/bin/bash
# Build script for MIDI Pushover Notifier macOS app

echo "MIDI Pushover Notifier - Build Script"
echo "====================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# Change to build directory
cd "$SCRIPT_DIR"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.egg-info
echo -e "${GREEN}✓${NC} Cleaned build directories"

# Create virtual environment for clean build
echo ""
echo "Creating build environment..."
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r "$PROJECT_ROOT/requirements.txt" > /dev/null 2>&1
pip install py2app > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencies installed"

# Build the app
echo ""
echo "Building application..."
python3 setup.py py2app > build.log 2>&1

# Check if build succeeded
if [ -d "dist/MIDI Pushover Notifier.app" ]; then
    echo -e "${GREEN}✓${NC} App built successfully!"
    
    # Sign with ad-hoc signature
    echo "Signing app..."
    codesign --force --deep --sign - "dist/MIDI Pushover Notifier.app" 2>/dev/null
    echo -e "${GREEN}✓${NC} App signed"
    
    # Get app size
    APP_SIZE=$(du -sh "dist/MIDI Pushover Notifier.app" | cut -f1)
    echo -e "${GREEN}✓${NC} App size: $APP_SIZE"
    
    # Deactivate virtual environment
    deactivate
    
    # Create DMG for distribution
    echo ""
    echo "Creating DMG..."
    
    # Create temp directory
    mkdir -p dmg_temp
    cp -r "dist/MIDI Pushover Notifier.app" dmg_temp/
    
    # Create a simple README for DMG
    cat > dmg_temp/README.txt << 'EOF'
MIDI Pushover Notifier
=====================

To install:
1. Drag "MIDI Pushover Notifier" to your Applications folder
2. Double-click to run
3. Look for the 🎹 icon in your menu bar

For setup instructions and documentation, visit:
https://github.com/yourusername/midi-pushover-notifier

EOF
    
    # Create DMG
    hdiutil create -volname "MIDI Pushover Notifier" \
        -srcfolder dmg_temp -ov -format UDZO \
        "MIDIPushoverNotifier.dmg" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} DMG created: MIDIPushoverNotifier.dmg"
        DMG_SIZE=$(du -sh MIDIPushoverNotifier.dmg | cut -f1)
        echo -e "${GREEN}✓${NC} DMG size: $DMG_SIZE"
    fi
    
    # Cleanup
    rm -rf dmg_temp build_env
    
    echo ""
    echo "====================================="
    echo -e "${GREEN}Build complete!${NC}"
    echo ""
    echo "Files created:"
    echo "  - dist/MIDI Pushover Notifier.app"
    echo "  - MIDIPushoverNotifier.dmg"
    
else
    echo -e "${RED}✗${NC} Build failed!"
    echo "Check build.log for details"
    deactivate
    rm -rf build_env
    exit 1
fi
