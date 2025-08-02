#!/usr/bin/env python3
"""
MIDI Pushover App with simplified MIDI learn
"""
import rumps
import mido
import requests
import json
import threading
import time
import os

CONFIG_PATH = os.path.expanduser("~/.midi_pushover_config.json")

class SimpleMidiApp(rumps.App):
    def __init__(self):
        super(SimpleMidiApp, self).__init__("MIDI", quit_button=None)
        self.midi_input = None
        self.is_listening = False
        self.last_midi_note = None
        self.waiting_for_midi = False
        
        # Load configuration
        self.load_config()
        
        # Create menu
        self.create_menu()
        
        # Auto-connect if device was saved
        if self.config.get("selected_device"):
            self.connect_midi_device(self.config["selected_device"])
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "pushover_user_key": "",
                "pushover_api_token": "",
                "selected_device": None,
                "midi_mappings": {
                    "60": {"message": "Stage needs assistance!", "priority": 1},
                    "62": {"message": "Technical issue on stage", "priority": 0},
                    "64": {"message": "Sound check requested", "priority": -1}
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_menu(self):
        """Create the menu"""
        # Status
        self.status_item = rumps.MenuItem("Status: Disconnected")
        self.menu.add(self.status_item)
        self.menu.add(rumps.separator)
        
        # MIDI Devices
        self.midi_menu = rumps.MenuItem("MIDI Devices")
        self.menu.add(self.midi_menu)
        
        # Mappings
        self.mappings_menu = rumps.MenuItem("Button Mappings")
        self.menu.add(self.mappings_menu)
        
        # Add mapping using last note
        self.menu.add(rumps.MenuItem("Map Last Note", callback=self.map_last_note))
        
        # Settings
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Pushover Settings", callback=self.configure_pushover))
        self.menu.add(rumps.MenuItem("Test Notification", callback=self.test_notification))
        
        # Quit
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))
        
        # Now populate submenus
        self.refresh_midi_devices()
        self.update_mappings_menu()
    
    def refresh_midi_devices(self):
        """Refresh MIDI devices list"""
        # Clear existing items
        while len(self.midi_menu) > 0:
            self.midi_menu.popitem()
            
        try:
            devices = mido.get_input_names()
            for device in devices:
                item = rumps.MenuItem(device, callback=self.device_clicked)
                if device == self.config.get("selected_device"):
                    item.state = True
                self.midi_menu.add(item)
        except:
            self.midi_menu.add(rumps.MenuItem("No devices found"))
    
    def device_clicked(self, sender):
        """Handle device selection"""
        device_name = sender.title
        self.connect_midi_device(device_name)
    
    def connect_midi_device(self, device_name):
        """Connect to MIDI device"""
        try:
            if self.midi_input:
                self.midi_input.close()
                self.is_listening = False
                time.sleep(0.1)
            
            self.midi_input = mido.open_input(device_name)
            self.is_listening = True
            
            # Start listening thread
            thread = threading.Thread(target=self.midi_listen_loop)
            thread.daemon = True
            thread.start()
            
            self.status_item.title = f"Status: Connected to {device_name}"
            self.config["selected_device"] = device_name
            self.save_config()
            
            # Update menu checkmarks
            for item in self.midi_menu.values():
                item.state = item.title == device_name
                
        except Exception as e:
            rumps.alert("Connection Error", str(e))
    
    def midi_listen_loop(self):
        """Listen for MIDI messages"""
        print("MIDI listen loop started")
        while self.is_listening and self.midi_input:
            try:
                for msg in self.midi_input.iter_pending():
                    print(f"\nRaw MIDI message: {msg}")
                    if msg.type == 'note_on' and msg.velocity > 0:
                        print(f"MIDI Note ON: {msg.note}, velocity: {msg.velocity}")
                        self.last_midi_note = msg.note
                        self.handle_midi_note(msg.note)
                    elif msg.type == 'note_off':
                        print(f"MIDI Note OFF: {msg.note}")
                time.sleep(0.01)
            except Exception as e:
                print(f"MIDI loop error: {e}")
                time.sleep(0.1)
        print("MIDI listen loop ended")
    
    def handle_midi_note(self, note):
        """Handle MIDI note"""
        note_str = str(note)
        print(f"\n=== MIDI Note Handler ===")
        print(f"Note: {note}, Note string: '{note_str}'")
        print(f"Waiting for MIDI: {self.waiting_for_midi}")
        print(f"Mappings: {self.config['midi_mappings']}")
        print(f"Note in mappings: {note_str in self.config['midi_mappings']}")
        
        if self.waiting_for_midi:
            # We're in learn mode
            self.waiting_for_midi = False
            rumps.notification("MIDI Learn", f"Note {note} detected", "Use 'Map Last Note' to assign a message")
            self.status_item.title = f"Status: Last note = {note}"
        elif note_str in self.config["midi_mappings"]:
            # Send notification
            mapping = self.config["midi_mappings"][note_str]
            print(f"Found mapping: {mapping}")
            print(f"Sending notification: {mapping['message']}")
            self.send_pushover_notification(mapping["message"], mapping.get("priority", 0))
        else:
            print(f"No mapping found for note {note_str}")
    
    def map_last_note(self, sender):
        """Map the last pressed note"""
        if self.last_midi_note is None:
            rumps.alert("No Note", "Press a note on your MIDI controller first, then use this option")
            return
        
        # Get message
        response = rumps.Window(
            title=f"Map Note {self.last_midi_note}",
            message="Enter the notification message:",
            default_text="Stage notification",
            ok="Save",
            cancel="Cancel"
        ).run()
        
        if response.clicked:
            # Get priority
            priority_response = rumps.Window(
                title="Priority",
                message="Priority Level:\n-2: Lowest (no notification)\n-1: Low (no sound)\n 0: Normal\n 1: High (bypass quiet hours)\n 2: Emergency (requires acknowledgment)",
                default_text="0",
                ok="Save",
                cancel="Cancel"
            ).run()
            
            priority = 0
            if priority_response.clicked:
                try:
                    priority = int(priority_response.text)
                    priority = max(-2, min(2, priority))
                except:
                    priority = 0
            
            # Save mapping
            self.config["midi_mappings"][str(self.last_midi_note)] = {
                "message": response.text,
                "priority": priority
            }
            self.save_config()
            
            # Reload config to ensure it's fresh
            self.load_config()
            
            self.update_mappings_menu()
            rumps.alert("Success", f"Note {self.last_midi_note} mapped to: {response.text}")
            
            # Debug: print current mappings
            print(f"\nCurrent mappings after save:")
            for note, mapping in self.config["midi_mappings"].items():
                print(f"  Note {note}: {mapping}")
    
    def update_mappings_menu(self):
        """Update mappings menu"""
        # Clear existing items
        while len(self.mappings_menu) > 0:
            self.mappings_menu.popitem()
        
        for note, mapping in self.config["midi_mappings"].items():
            title = f"Note {note}: {mapping['message']}"
            self.mappings_menu.add(rumps.MenuItem(title))
        
        self.mappings_menu.add(rumps.separator)
        self.mappings_menu.add(rumps.MenuItem("Listen for Next Note", callback=self.listen_for_note))
        self.mappings_menu.add(rumps.MenuItem("Clear All", callback=self.clear_mappings))
    
    def listen_for_note(self, sender):
        """Start listening for a note"""
        self.waiting_for_midi = True
        self.status_item.title = "Status: Press a MIDI note..."
        rumps.notification("MIDI Learn", "Press a note", "Then use 'Map Last Note' menu item")
    
    def clear_mappings(self, sender):
        """Clear all mappings"""
        if rumps.alert("Clear All Mappings", "Are you sure?", ok="Clear", cancel="Cancel"):
            self.config["midi_mappings"] = {}
            self.save_config()
            self.update_mappings_menu()
    
    def configure_pushover(self, sender):
        """Configure Pushover"""
        # User key
        user_response = rumps.Window(
            title="Pushover User Key",
            message="Enter your User Key:",
            default_text=self.config.get("pushover_user_key", ""),
            ok="Next",
            cancel="Cancel"
        ).run()
        
        if user_response.clicked:
            # API token
            token_response = rumps.Window(
                title="Pushover API Token",
                message="Enter your API Token:",
                default_text=self.config.get("pushover_api_token", ""),
                ok="Save",
                cancel="Cancel"
            ).run()
            
            if token_response.clicked:
                self.config["pushover_user_key"] = user_response.text
                self.config["pushover_api_token"] = token_response.text
                self.save_config()
                rumps.alert("Saved", "Pushover credentials saved")
    
    def send_pushover_notification(self, message, priority=0):
        """Send Pushover notification"""
        print(f"\n=== SENDING PUSHOVER NOTIFICATION ===")
        print(f"Message: {message}")
        print(f"Priority: {priority}")
        print(f"User Key: {self.config.get('pushover_user_key', 'NOT SET')[:8]}...")
        print(f"API Token: {self.config.get('pushover_api_token', 'NOT SET')[:8]}...")
        
        if not self.config.get("pushover_user_key") or not self.config.get("pushover_api_token"):
            print("ERROR: Missing Pushover credentials!")
            rumps.alert("Error", "Please configure Pushover first")
            return
        
        try:
            data = {
                "token": self.config["pushover_api_token"],
                "user": self.config["pushover_user_key"],
                "message": message,
                "title": "Stage Alert",
                "priority": priority
            }
            
            # Emergency priority (2) requires retry and expire parameters
            if priority == 2:
                data["retry"] = 30  # Retry every 30 seconds
                data["expire"] = 3600  # Expire after 1 hour
                print("Adding emergency parameters (retry=30, expire=3600)")
            
            print(f"Sending to Pushover API...")
            
            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data=data,
                timeout=10
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                print("✓ Notification sent successfully!")
                rumps.notification("Success", "Notification sent", message[:50])
            else:
                print(f"✗ Error: {response.text}")
                rumps.alert("Pushover Error", f"Failed to send: {response.text}")
        except Exception as e:
            print(f"✗ Exception: {type(e).__name__}: {e}")
            rumps.alert("Error", f"Failed to send notification: {str(e)}")
    
    def test_notification(self, sender):
        """Send test notification"""
        self.send_pushover_notification("Test notification from MIDI Pushover", 0)

if __name__ == "__main__":
    SimpleMidiApp().run()
