# Building MIDI Pushover Notifier

This directory contains the build scripts and configuration for creating a standalone macOS application.

## Prerequisites

- macOS 10.12 or later
- Python 3.6 or later
- Xcode Command Line Tools

## Build Instructions

1. From the project root, navigate to the build directory:
   ```bash
   cd build
   ```

2. Run the build script:
   ```bash
   ./build_app.sh
   ```

3. The script will:
   - Create a clean virtual environment
   - Install all dependencies
   - Build the macOS app
   - Sign it with an ad-hoc signature
   - Create a DMG for distribution

4. Find the built files:
   - App: `dist/MIDI Pushover Notifier.app`
   - DMG: `MIDIPushoverNotifier.dmg`

## Manual Build

If you prefer to build manually:

```bash
# Install py2app
pip3 install py2app

# Install dependencies
pip3 install -r ../requirements.txt

# Build the app
python3 setup.py py2app

# Sign the app (optional but recommended)
codesign --force --deep --sign - "dist/MIDI Pushover Notifier.app"
```

## Troubleshooting

### Build Fails
- Check `build.log` for detailed error messages
- Ensure all dependencies are installed
- Try building in a clean virtual environment

### Code Signing Issues
- The build script uses ad-hoc signing which should work for local distribution
- For App Store or notarization, you'll need a Developer ID certificate

### Icon Not Showing
- Ensure `logo.icns` exists in the `assets` directory
- The icon should be in proper .icns format (not just renamed)

## Distribution

The DMG file is ready for distribution. Users can:
1. Download the DMG
2. Open it
3. Drag the app to their Applications folder
4. Run it (may need to right-click and select "Open" first time)
