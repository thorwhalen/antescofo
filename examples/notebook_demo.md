# Antescofo Demo - Jupyter Notebook

Quick demo notebook for testing Antescofo with Pure Data.

**Note**: Some async features may not work perfectly in notebooks due to event loop conflicts. 
For best results, use the `examples/run_demo.py` script instead.

## Setup

First, make sure your config is initialized:

```python
from antescofo import init_config, print_config

# Initialize config (creates ~/.config/antescofo/config.json)
init_config()

# View current config
print_config()
```

## Generate a Score

```python
from pathlib import Path
from antescofo import ScoreBuilder

# Create a simple score
score_path = Path("demo_score.asco.txt")

builder = (
    ScoreBuilder()
    .comment("Notebook Demo Score")
    .raw("@global $volume := 0.5")
    .raw("")
    .comment("Note 1: C4")
    .event("NOTE", 1.0, "C4 60")
    .action('OSC "/synth/play" 440 $volume')
    .action('print "Playing C4"')
    .raw("")
    .comment("Note 2: E4")
    .event("NOTE", 1.0, "E4 64")
    .action('OSC "/synth/play" 660 $volume')
    .action('print "Playing E4"')
    .raw("")
    .comment("Stop")
    .event("NOTE", 0.5, "G4 67")
    .action('OSC "/synth/stop" 0')
    .action('print "Done"')
)

builder.save(score_path)
print(f"✓ Score saved to {score_path}")
```

## Prerequisites Check

Before running the demo, ensure:

```python
print("""
CHECKLIST:
----------
□ Pure Data is running
□ pd_synth_patch.pd is open in PD
□ Clicked Antescofo config messages in patch:
  - incomingosc 1
  - incomingoscport 5678
  - ascographconf localhost 9999
  - calibrate
□ DSP is ON (Media → DSP On)

Press Enter when ready...
""")
```

## Run Demo (Simple Version)

```python
from antescofo import AntescofoClient, EventType

# Create client (uses config automatically)
client = AntescofoClient()

# Connect
print("Connecting...")
client.connect()
print(f"✓ Connected to {client.host}:{client.port}")

# Load score
print(f"Loading score: {score_path}")
client.load_score(score_path.resolve())
print("✓ Score loaded")

# Start playback
print("▶ Starting playback... (you should hear tones)")
client.start()
```

## Control Playback

```python
# Change tempo
import time

time.sleep(2)
print("Setting tempo to 150 BPM")
client.set_tempo(150.0)

time.sleep(3)

# Stop
print("⏹ Stopping")
client.stop()
```

## Cleanup

```python
# Disconnect
client.disconnect()
print("✓ Disconnected")
```

## Listen to Events (Advanced)

If you want to see events from Antescofo:

```python
from antescofo import AntescofoClient, EventType, Event

def on_action(event: Event):
    print(f"  [ACTION] {event.data}")

def on_tempo(event: Event):
    print(f"  [TEMPO] {event.data} BPM")

# Create new client with event listening
client = AntescofoClient()
client.connect()

# Subscribe to events
client.on(EventType.ACTION_TRACE, on_action)
client.on(EventType.TEMPO, on_tempo)

# Load and play
client.load_score(score_path.resolve())
print("Playing with event monitoring...")
client.start()
```

## Recommended: Use the Script Instead

For a more reliable experience, run the script from terminal:

```bash
python examples/run_demo.py
```

This avoids potential event loop issues in Jupyter notebooks.
