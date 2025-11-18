# Antescofo Python Interface

A comprehensive Python library for communicating with and controlling [Antescofo](https://antescofo-doc.ircam.fr/), the score following and synchronous programming language for music developed at IRCAM.

## Features

- **OSC Communication**: Send and receive OSC messages to/from Antescofo instances
- **Transport Control**: Load scores, start/stop playback, control tempo, navigate events
- **Event System**: Subscribe to and handle events from Antescofo (tempo changes, beat positions, action traces, etc.)
- **Score Generation**: Programmatically create and manipulate Antescofo score files
- **Data Types**: Python representations of Antescofo data structures (Tabs, Maps)
- **Type-Safe**: Well-typed API with comprehensive error handling
- **Easy to Use**: Pythonic interface with context manager support

## Installation

### Prerequisites

**Important**: This Python library is a **client** that communicates with Antescofo. You must have Antescofo itself running before you can use this library.

You need one of the following:
- **Antescofo for Max/MSP**: The `antescofo~` external object in Max/MSP
- **Antescofo for PureData**: The `antescofo` external in PureData
- **Antescofo Standalone**: The standalone Antescofo application

Download Antescofo from [IRCAM Forum](https://forum.ircam.fr/projects/detail/antescofo/) or see the [official documentation](https://antescofo-doc.ircam.fr/).

### Installing the Python Client

#### From PyPI (when published)

```bash
pip install antescofo
```

#### From Source

```bash
git clone https://github.com/yourusername/antescofo.git
cd antescofo
pip install -e .
```

### Python Dependencies

- Python >= 3.8
- python-osc >= 1.8.0

### Verifying Your Setup

Before using this Python library:

1. **Start Antescofo** (Max/MSP, PureData, or standalone)
2. **Configure OSC ports** in Antescofo:
   - Default Antescofo receive port: 5678
   - Default Ascograph port: 6789 (for receiving events)
3. **Test the connection** with the Python client (see Quick Start below)

If you get connection errors, verify that:
- Antescofo is running
- The ports match between Antescofo and your Python code
- No firewall is blocking localhost connections

## Quick Start

### Basic Control

```python
from antescofo import AntescofoClient

# Create and connect to Antescofo
with AntescofoClient(host="localhost", port=5678) as client:
    # Load a score
    client.load_score("path/to/score.asco.txt")

    # Start playback
    client.start()

    # Set tempo
    client.set_tempo(120)

    # Wait for some time
    client.wait(5)

    # Stop playback
    client.stop()
```

### Event Listening

```python
from antescofo import AntescofoClient, EventType

# Create client with receive port to get events
client = AntescofoClient(
    host="localhost",
    port=5678,
    receive_port=9999  # Port to receive events on
)

# Define event handlers
def on_tempo_change(event):
    print(f"Tempo changed to: {event.data}")

def on_beat_position(event):
    print(f"Beat position: {event.data}")

# Connect and subscribe
client.connect()
client.on(EventType.TEMPO, on_tempo_change)
client.on(EventType.BEAT_POSITION, on_beat_position)

# Start playback
client.start()

# Keep running to receive events
try:
    while True:
        client.wait(0.1)
except KeyboardInterrupt:
    client.stop()
    client.disconnect()
```

### Score Generation

```python
from antescofo import ScoreBuilder

# Build a score programmatically
builder = (
    ScoreBuilder()
    .comment("My Generated Score")
    .event("NOTE", 1.0, "C4 60")
    .action('print "Hello from C4"')
    .event("NOTE", 0.5, "D4 62")
    .action('$tempo := 120')
    .event("NOTE", 0.5, "E4 64")
    .action('print "Finished!"')
)

# Save to file
builder.save("generated_score.asco.txt")

# Or get the score object
score = builder.get_score()
print(score)
```

## Documentation

### AntescofoClient

The main interface for controlling Antescofo.

```python
client = AntescofoClient(
    host="localhost",        # Antescofo host
    port=5678,              # Port to send messages to
    receive_port=None,      # Port to receive events (optional)
    auto_connect=False      # Auto-connect on initialization
)
```

#### Transport Control Methods

- `connect()` - Connect to Antescofo
- `disconnect()` - Disconnect from Antescofo
- `load_score(filepath)` - Load a score file
- `start()` - Start playback
- `stop()` - Stop playback
- `pause()` - Pause playback
- `resume()` - Resume paused playback
- `next_event()` - Skip to next event
- `prev_event()` - Go to previous event
- `set_tempo(bpm)` - Set tempo in BPM

#### Event Subscription

- `on(event_type, handler)` - Subscribe to events
- `off(event_type, handler)` - Unsubscribe from events

#### OSC Communication

- `send_osc(address, *args)` - Send OSC message
- `enable_osc_communication(enable=True)` - Enable/disable OSC
- `configure_ascograph(host, port)` - Configure Ascograph connection

### Event Types

Available event types:

- `EventType.STOP` - Playback stopped
- `EventType.BEAT_POSITION` - Beat position update
- `EventType.RNOW` - Relative time update
- `EventType.TEMPO` - Tempo change
- `EventType.PITCH` - Pitch detection
- `EventType.ACTION_TRACE` - Action execution trace
- `EventType.LOAD_SCORE` - Score loaded

### Data Types

#### Tab (Array/List)

```python
from antescofo import Tab

# Create a tab
tab = Tab([1, 2, 3, 4])

# Access elements
print(tab[0])  # 1

# Append
tab.append(5)

# Convert to/from list
lst = tab.to_list()
tab2 = Tab.from_list([10, 20, 30])
```

#### Map (Dictionary)

```python
from antescofo import Map

# Create a map
m = Map({"tempo": 120, "volume": 0.8})

# Access values
print(m["tempo"])  # 120

# Set values
m["pitch"] = 440

# Convert to/from dict
d = m.to_dict()
m2 = Map.from_dict({"key": "value"})
```

### Score Generation

#### ScoreFile

```python
from antescofo import ScoreFile

# Create a new score
score = ScoreFile()

# Add content
score.add_comment("My Score")
score.add_event("NOTE", 1.0, "C4 60")
score.add_action('print "Hello"')

# Insert other files
score.insert_file("library.asco.txt")
score.insert_file_once("utilities.asco.txt")

# Add conditionals
score.add_conditional(
    "@arch_darwin",
    'print "macOS"',
    'print "Other OS"'
)

# Save
score.save("myscore.asco.txt")

# Load existing score
loaded = ScoreFile.load("existing.asco.txt")
```

#### ScoreBuilder

```python
from antescofo import ScoreBuilder

# Use builder pattern for fluent API
builder = (
    ScoreBuilder()
    .comment("Generated Score")
    .event("NOTE", 1.0, "C4 60")
    .action('print "Hello"')
    .insert("library.asco.txt")
    .raw("@global $x := 42")  # Add raw line
)

builder.save("output.asco.txt")
```

## Examples

See the `examples/` directory for complete examples:

- `basic_control.py` - Basic playback control
- `event_listening.py` - Event subscription and handling
- `score_generation.py` - Programmatic score creation

## Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=antescofo --cov-report=html
```

## Architecture

The library is organized into several modules:

- `client.py` - High-level `AntescofoClient` interface
- `osc.py` - OSC communication layer using python-osc
- `events.py` - Event system and dispatcher
- `types.py` - Data type mappings (Tab, Map, etc.)
- `score.py` - Score file reading/writing/generation
- `constants.py` - Constants and message types
- `exceptions.py` - Custom exceptions

## Requirements

- **Antescofo**: You need a running Antescofo instance (Max/MSP external, PureData external, or standalone)
- **OSC Setup**: Configure Antescofo to communicate via OSC
  - Default Antescofo port: 5678
  - Default Ascograph port: 6789

## Antescofo Resources

- [Antescofo Documentation](https://antescofo-doc.ircam.fr/)
- [IRCAM Forum](https://forum.ircam.fr/projects/detail/antescofo/)
- [Function Library](https://antescofo-doc.ircam.fr/Library/Functions/00intro/)
- [OSC Protocol](https://antescofo-doc.ircam.fr/Reference/osc_internals/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Authors

- Antescofo Python Interface Contributors

## Acknowledgments

- Antescofo was developed by Arshia Cont and the team at IRCAM
- This Python interface is an independent project to facilitate Python integration
