"""
Setup script for building MIDI Pushover Notifier as a macOS app
"""
from setuptools import setup
import os
import sys

# Get the directory where this setup.py is located
SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETUP_DIR)

# Paths to the app and resources
APP = [os.path.join(PROJECT_ROOT, 'src', 'midi_pushover_notifier.py')]
DATA_FILES = [('', [os.path.join(PROJECT_ROOT, 'assets', 'logo.icns')])]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': os.path.join(PROJECT_ROOT, 'assets', 'logo.icns'),
    'plist': {
        'CFBundleName': 'MIDI Pushover Notifier',
        'CFBundleDisplayName': 'MIDI Pushover Notifier',
        'CFBundleGetInfoString': "Send Pushover notifications from MIDI controller",
        'CFBundleIdentifier': 'com.midipushover.notifier',
        'CFBundleVersion': "1.1.0",
        'CFBundleShortVersionString': "1.1.0",
        'NSHumanReadableCopyright': "Copyright © 2025",
        'NSHighResolutionCapable': True,
        'LSUIElement': True,  # Menu bar app (no dock icon)
        'LSMinimumSystemVersion': '10.12.0',
    },
    'packages': [
        'rumps',
        'mido',
        'rtmidi',
        'requests',
        'certifi',
        'charset_normalizer',
        'idna',
        'urllib3'
    ],
    'includes': [
        'rumps',
        'mido',
        'rtmidi',
        'requests',
        'json',
        'threading',
        'time',
        'os',
        'sys'
    ],
    'excludes': [
        'tkinter',
        'PyQt4',
        'PyQt5',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'test',
        'tests',
        'unittest',
        'xmlrpc'
    ],
    'optimize': 2,
    'compressed': True,
    'semi_standalone': False,
    'site_packages': True,
}

setup(
    name="MIDI Pushover Notifier",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
