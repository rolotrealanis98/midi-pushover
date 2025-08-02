# MIDI Pushover Notifier 🎹

A macOS menu bar application that sends push notifications to your devices when MIDI buttons are pressed. Perfect for live performers, stage technicians, and anyone who needs instant communication triggered by MIDI controllers.

![MIDI Pushover Notifier Icon](assets/logo.icns)

## Features

- **Menu Bar App**: Runs quietly in your macOS menu bar with a 🎹 icon
- **MIDI Device Support**: Works with any MIDI controller connected to your Mac
- **Easy MIDI Mapping**: Simple two-step process to map any MIDI note to a custom notification
- **Pushover Integration**: Sends instant push notifications to iOS/Android devices
- **Custom Messages**: Each MIDI button can have its own message and priority level
- **Auto-Reconnect**: Remembers your MIDI device and reconnects on startup

## Requirements

- macOS 10.12 (Sierra) or later
- Python 3.6 or later
- MIDI controller
- Pushover account and app

## Installation

### Option 1: Download Pre-built App (Recommended)

1. Download the latest release from the [Releases](https://github.com/yourusername/midi-pushover-notifier/releases) page
2. Open the DMG file and drag the app to your Applications folder
3. Right-click the app and select "Open" (first time only, to bypass Gatekeeper)

### Option 2: Build from Source

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/midi-pushover-notifier.git
   cd midi-pushover-notifier
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python3 src/midi_pushover_notifier.py
   ```

### Option 3: Build as macOS App

1. Install py2app:
   ```bash
   pip3 install py2app
   ```

2. Build the app:
   ```bash
   cd build
   ./build_app.sh
   ```

3. Find the built app in `dist/MIDI Pushover Notifier.app`

## Setup

### 1. Pushover Configuration

1. Create a [Pushover](https://pushover.net) account if you don't have one
2. Install the Pushover app on your iOS or Android device
3. Create a new application in Pushover (name it "MIDI Controller" or similar)
4. Note your User Key and API Token

### 2. First Run

1. Launch MIDI Pushover Notifier
2. Look for the 🎹 icon in your menu bar
3. Click the icon and go to **Pushover Settings**
4. Enter your User Key and API Token
5. Click **Test Notification** to verify it's working

### 3. Connect MIDI Device

1. Connect your MIDI controller to your Mac
2. Click the 🎹 icon → **MIDI Devices**
3. Select your controller from the list

## Usage

### Mapping MIDI Buttons

The app uses a simple two-step process to avoid threading issues:

1. **Press a MIDI button** on your controller
2. Click **Map Last Note** in the menu
3. Enter the notification message
4. Set the priority level (-2 to 2)

Alternative method:
1. Click **Button Mappings** → **Listen for Next Note**
2. Press a MIDI button
3. Click **Map Last Note**

### Priority Levels

- **2 (Emergency)**: Bypasses Do Not Disturb, repeats until acknowledged
- **1 (High)**: Bypasses quiet hours
- **0 (Normal)**: Standard notification
- **-1 (Low)**: No sound/vibration
- **-2 (Lowest)**: No notification, just badge

### Default Mappings

The app comes with three default mappings:
- **Note 60 (Middle C)**: "Stage needs assistance!" (High priority)
- **Note 62 (D)**: "Technical issue on stage" (Normal priority)
- **Note 64 (E)**: "Sound check requested" (Low priority)

## Troubleshooting

### MIDI Device Not Showing
- Ensure your MIDI controller is connected before starting the app
- Try unplugging and reconnecting the device
- Check that no other app is using the MIDI device exclusively

### Notifications Not Received
- Verify your Pushover credentials are correct
- Test with the "Test Notification" option first
- Check that the Pushover app is installed and logged in on your device
- Ensure your device has an internet connection

### App Won't Start
- Make sure you have Python 3.6 or later installed
- Install all required dependencies: `pip3 install -r requirements.txt`
- On first run, right-click and select "Open" to bypass macOS security

## Auto-Start on Login

To have the app start automatically:

1. Open **System Preferences** → **Users & Groups**
2. Select your user and click **Login Items**
3. Click the **+** button
4. Navigate to Applications and select **MIDI Pushover Notifier**

## Development

### Project Structure

```
midi-pushover-notifier/
├── src/
│   └── midi_pushover_notifier.py   # Main application code
├── assets/
│   └── logo.icns                   # Application icon
├── build/
│   ├── build_app.sh               # Build script for macOS app
│   └── setup.py                   # py2app configuration
├── docs/
│   └── CONTRIBUTING.md            # Contribution guidelines
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
└── README.md                      # This file
```

### Building the App

See the [build documentation](build/README.md) for detailed build instructions.

### Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [rumps](https://github.com/jaredks/rumps) for macOS menu bar integration
- Uses [mido](https://github.com/mido/mido) for MIDI handling
- Notifications powered by [Pushover](https://pushover.net)

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Look through existing [Issues](https://github.com/yourusername/midi-pushover-notifier/issues)
3. Create a new issue with details about your problem

---

Made with ❤️ for musicians and stage technicians
