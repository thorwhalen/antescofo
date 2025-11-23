#!/usr/bin/env python
"""
Quick Reference - Antescofo Python Usage

Common code snippets for working with Antescofo.
"""

# ============================================================================
# BASIC USAGE
# ============================================================================

# Import
from antescofo import AntescofoClient

# Create client (uses ~/.config/antescofo/config.json)
client = AntescofoClient()

# Connect
client.connect()

# Load and play a score
client.load_score("myscore.asco.txt")
client.start()

# Control playback
client.set_tempo(120.0)
client.pause()
client.resume()
client.stop()

# Disconnect
client.disconnect()


# ============================================================================
# CONFIGURATION
# ============================================================================

from antescofo import print_config, get_config_value, set_config_value

# View config
print_config()

# Get value
port = get_config_value("antescofo_send_port")

# Set value
set_config_value("antescofo_send_port", 6000)


# ============================================================================
# EVENT LISTENING
# ============================================================================

from antescofo import AntescofoClient, EventType, Event


def on_action(event: Event):
    print(f"Action: {event.data}")


def on_tempo(event: Event):
    print(f"Tempo: {event.data} BPM")


client = AntescofoClient()
client.connect()

# Subscribe to events
client.on(EventType.ACTION_TRACE, on_action)
client.on(EventType.TEMPO, on_tempo)

client.load_score("myscore.asco.txt")
client.start()

# Keep script alive
client.wait(10)  # Wait 10 seconds

client.disconnect()


# ============================================================================
# SCORE GENERATION
# ============================================================================

from antescofo import ScoreBuilder
from pathlib import Path

# Build a score
score = (
    ScoreBuilder()
    .comment("My Score")
    .raw("@global $volume := 0.5")
    .event("NOTE", 1.0, "C4 60")
    .action('OSC "/synth/play" 440 $volume')
    .action('print "Playing C4"')
    .event("NOTE", 1.0, "E4 64")
    .action('OSC "/synth/play" 660 $volume')
    .action('print "Playing E4"')
)

# Save to file
score.save("myscore.asco.txt")

# Or get as string
score_text = str(score)


# ============================================================================
# CONTEXT MANAGER (Auto-connect/disconnect)
# ============================================================================

from antescofo import AntescofoClient

with AntescofoClient() as client:
    client.load_score("myscore.asco.txt")
    client.start()
    client.wait(5)
    client.stop()
# Automatically disconnected


# ============================================================================
# CUSTOM PORTS (Override config)
# ============================================================================

from antescofo import AntescofoClient

# Use specific ports (ignores config)
client = AntescofoClient(
    host="localhost",
    port=6000,  # Send commands to this port
    receive_port=8000,  # Receive events on this port
)

client.connect()
# ... use client ...
client.disconnect()


# ============================================================================
# SEND RAW OSC MESSAGES
# ============================================================================

from antescofo import AntescofoClient

client = AntescofoClient()
client.connect()

# Send OSC message (automatically prefixes with /antescofo/)
client.send_osc("mycommand", 123, "hello")
# Sends: /antescofo/mycommand 123 "hello"

# Or specify full address
client.send_osc("/antescofo/custom", 42)

client.disconnect()


# ============================================================================
# PURE DATA SETUP CHECKLIST
# ============================================================================

"""
Before running any script:

1. Open Pure Data
2. Open: antescofo/pd_synth_patch.pd
3. Click message boxes:
   - incomingosc 1
   - incomingoscport 5678
   - ascographconf localhost 9999
   - calibrate
4. Enable DSP (Media → DSP On)
5. Keep PD running

Then run your Python script.
"""


# ============================================================================
# PORT CONFIGURATION
# ============================================================================

"""
Config file: ~/.config/antescofo/config.json

Key settings:
- antescofo_send_port: 5678     (Python → Antescofo)
- python_receive_port: 9999     (Antescofo → Python)
- pd_listen_port: 10000         (Antescofo → PD Synth)

These MUST match the ports in your PD patch:
- incomingoscport 5678
- ascographconf localhost 9999
- netreceive 10000
"""


# ============================================================================
# QUICK START
# ============================================================================

"""
1. Setup config:
   python examples/setup_config.py

2. Setup PD:
   - Open pd_synth_patch.pd
   - Click config messages
   - Enable DSP

3. Run demo:
   python examples/run_demo.py

4. You should HEAR tones!
"""

if __name__ == "__main__":
    print(__doc__)
    print("\nThis file contains code snippets for reference.")
    print("Copy and paste the sections you need into your own scripts.")
    print("\nFor a complete working example, run:")
    print("  python examples/run_demo.py")
