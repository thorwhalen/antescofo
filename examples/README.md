# Antescofo Examples

This directory contains example scripts showing how to use the Antescofo Python library.

## Quick Start

### 1. Setup Configuration

First, initialize your Antescofo configuration:

```bash
python examples/setup_config.py
```

This creates `~/.config/antescofo/config.json` with default settings:
- **antescofo_send_port**: 5678 (where Python sends commands to Antescofo)
- **python_receive_port**: 9999 (where Python receives events from Antescofo)
- **pd_listen_port**: 10000 (where PD synth receives OSC messages)

### 2. Setup Pure Data

Before running the demo:

1. **Open Pure Data** (Pd)
2. **Open the patch**: `antescofo/pd_synth_patch.pd`
3. **Configure Antescofo**: Click the message boxes under "- A N T E S C O F O -":
   - `incomingosc 1`
   - `incomingoscport 5678`
   - `ascographconf localhost 9999`
   - `calibrate`
4. **Enable DSP**: Menu → Media → DSP On
5. Leave the patch running

### 3. Run the Demo

```bash
python examples/run_demo.py
```

This will:
- Generate a simple score file (`simple_demo_score.asco.txt`)
- Connect to Antescofo (running in PD)
- Load and play the score
- Send OSC messages to the PD synth
- **You should HEAR tones** (C, E, G progression)

## Examples Overview

### Core Examples

- **`run_demo.py`**: Complete end-to-end demo (RECOMMENDED START HERE)
- **`setup_config.py`**: Initialize user configuration

### Learning Examples

- **`basic_control.py`**: Basic transport control (start, stop, tempo)
- **`event_listening.py`**: Subscribe to Antescofo events
- **`score_generation.py`**: Generate score files programmatically
- **`antescofo_example_script.py`**: Original example script

## Configuration

### View Current Config

```python
from antescofo import print_config
print_config()
```

### Modify Config

Edit `~/.config/antescofo/config.json` directly, or use Python:

```python
from antescofo import set_config_value

set_config_value("antescofo_send_port", 6000)
set_config_value("python_receive_port", 8000)
```

### Config Location

The config file is stored at:
```
~/.config/antescofo/config.json
```

## Troubleshooting

### "No sound" or "Connection failed"

1. **Check Pure Data is running** with `pd_synth_patch.pd` open
2. **Verify ports match** between your config and the PD patch:
   - PD patch: Look at the `incomingoscport` and `ascographconf` messages
   - Python config: Run `python -c "from antescofo import print_config; print_config()"`
3. **Check DSP is ON** in Pure Data (Menu → Media → DSP On)
4. **Verify Antescofo external loaded**: You should see `[antescofo~]` object in the patch

### "Score file not found"

The demo script generates the score automatically. If you see this error:
```bash
python -c "from antescofo import ScoreBuilder; ScoreBuilder().save('simple_demo_score.asco.txt')"
```

### Port Conflicts

If ports are already in use, modify your config:
```bash
# Edit ~/.config/antescofo/config.json
# Change the port numbers to available ports
# Then update the corresponding ports in your PD patch
```

## More Information

- **Antescofo Documentation**: https://antescofo-doc.ircam.fr/
- **Package Documentation**: See main README.md
- **PD Patch Info**: See comments in `antescofo/pd_synth_patch.pd`
