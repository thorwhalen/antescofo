# Getting Started with Antescofo Python Client

## What is This?

The `antescofo` Python package is a **client library** that communicates with the Antescofo music score following system. It does **NOT** produce sound itself - it only sends commands to and receives events from an Antescofo instance.

## Your Current Setup Status

### ✅ What You Have
- Python package `antescofo` installed
- Demo notebook with examples

### ❌ What You Still Need
- **Antescofo application** (Max/MSP external, PureData external, or standalone)
- A running instance of Antescofo configured for OSC communication

## Step-by-Step Setup Guide

### 1. Get Antescofo (The Application)

You need one of these options:

#### Option A: Antescofo for Max/MSP (Most Common)
1. Download Max/MSP from: https://cycling74.com/
2. Download the `antescofo~` external from: https://forum.ircam.fr/projects/detail/antescofo/
3. Install the external in Max/MSP

#### Option B: Antescofo for PureData
1. Download PureData from: https://puredata.info/
2. Download the `antescofo` external from: https://forum.ircam.fr/projects/detail/antescofo/
3. Install the external in PureData

#### Option C: Antescofo Standalone
1. Download the standalone application from: https://forum.ircam.fr/projects/detail/antescofo/

### 2. Configure Antescofo for OSC Communication

Once you have Antescofo running:

1. **Enable OSC communication** in Antescofo
2. **Set the receive port** to `5678` (default)
3. **Set the send port** (for events) to `6789` or `9999`

### 3. Test the Connection

Run this Python code to verify connection:

```python
from antescofo import AntescofoClient

try:
    client = AntescofoClient(host="localhost", port=5678)
    client.connect()
    print("✅ Successfully connected!")
    client.disconnect()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

If this fails, check:
- Is Antescofo running?
- Is it listening on port 5678?
- Is your firewall blocking localhost connections?

### 4. Create Your First Score

```python
from antescofo import ScoreBuilder

# Generate a simple score
score = (
    ScoreBuilder()
    .comment("My First Score")
    .event("NOTE", 1.0, "C4 60")
    .action('print "Hello from C4"')
    .event("NOTE", 1.0, "D4 62")
    .action('print "Hello from D4"')
)

score.save("my_first_score.asco.txt")
print("✅ Score saved!")
```

### 5. Play Your Score

```python
from antescofo import AntescofoClient

with AntescofoClient(host="localhost", port=5678) as client:
    client.load_score("my_first_score.asco.txt")
    client.start()
    client.wait(5)  # Wait 5 seconds
    client.stop()
```

**Note:** Sound comes from Antescofo (Max/MSP/PureData), not Python!

## Architecture Overview

```
┌─────────────────────┐
│   Your Python Code  │
│  (antescofo pkg)    │
└──────────┬──────────┘
           │ OSC Messages
           │ (Commands & Events)
           │
┌──────────▼──────────┐
│    Antescofo        │
│  (Max/MSP/PD/       │
│   Standalone)       │
└──────────┬──────────┘
           │
           ▼
      🔊 Audio Output
```

## Common Issues and Solutions

### "Connection refused" Error
**Problem:** Python can't connect to Antescofo
**Solution:** 
1. Make sure Antescofo is running
2. Check that it's listening on port 5678
3. Verify OSC communication is enabled

### "No sound" Issue
**Problem:** Code runs but you hear nothing
**Solution:** 
- Remember: Python doesn't produce sound!
- Sound comes from Antescofo (Max/MSP/PureData/Standalone)
- Check that Antescofo's audio output is configured
- Verify your system's audio settings

### "File not found" Error
**Problem:** Can't load score file
**Solution:**
1. Use absolute paths: `os.path.abspath("score.asco.txt")`
2. Or generate scores programmatically with `ScoreBuilder`
3. Check file exists: `os.path.exists("score.asco.txt")`

### Event Listening Doesn't Work
**Problem:** Not receiving events from Antescofo
**Solution:**
1. Specify `receive_port` when creating client
2. Configure Antescofo to send events to that port
3. Enable Ascograph communication in Antescofo

## Example Workflows

### Workflow 1: Simple Playback
```python
from antescofo import AntescofoClient, ScoreBuilder

# 1. Generate score
score = ScoreBuilder().event("NOTE", 1.0, "C4 60").action('print "C4"')
score.save("test.asco.txt")

# 2. Play it
with AntescofoClient() as client:
    client.load_score("test.asco.txt")
    client.start()
    client.wait(3)
    client.stop()
```

### Workflow 2: Interactive Control
```python
from antescofo import AntescofoClient

client = AntescofoClient()
client.connect()
client.load_score("my_score.asco.txt")
client.start()

# Control tempo dynamically
client.set_tempo(60)   # Slow
client.wait(2)
client.set_tempo(120)  # Medium
client.wait(2)
client.set_tempo(180)  # Fast

client.stop()
client.disconnect()
```

### Workflow 3: Event Listening
```python
from antescofo import AntescofoClient, EventType

client = AntescofoClient(receive_port=9999)
client.connect()

def on_beat(event):
    print(f"Beat: {event.data}")

client.on(EventType.BEAT_POSITION, on_beat)
client.start()

# Listen for 10 seconds
client.wait(10)
client.stop()
client.disconnect()
```

## Next Steps

1. **Read the full README.md** for comprehensive API documentation
2. **Explore the examples/** folder for more complex use cases
3. **Check Antescofo documentation** at https://antescofo-doc.ircam.fr/
4. **Try the demo notebook** at `misc/antescofo_demo.ipynb`

## Resources

- **Antescofo Official Site:** https://antescofo-doc.ircam.fr/
- **IRCAM Forum:** https://forum.ircam.fr/projects/detail/antescofo/
- **OSC Protocol Reference:** https://antescofo-doc.ircam.fr/Reference/osc_internals/
- **Python-OSC Documentation:** https://python-osc.readthedocs.io/

## Getting Help

If you're stuck:
1. Check this guide first
2. Review the examples in `examples/`
3. Consult the Antescofo documentation
4. Verify your Antescofo setup is working independently (outside Python)
5. Check OSC communication is properly configured

Remember: **Python is just the controller, Antescofo is the sound engine!**
