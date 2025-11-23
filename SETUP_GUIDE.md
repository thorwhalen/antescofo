# Antescofo Configuration Setup - Summary

## What Was Done

### 1. Created Configuration System

**File: `antescofo/util.py`**
- Manages user config at `~/.config/antescofo/config.json`
- Provides functions: `init_config()`, `load_config()`, `get_config_value()`, etc.
- Auto-initializes config with sensible defaults on first import
- Includes path resolution utilities

**Default Configuration:**
```json
{
  "antescofo_send_port": 5678,        // Python → Antescofo
  "python_receive_port": 9999,        // Antescofo → Python  
  "pd_listen_port": 10000,            // Python → PD Synth
  "pd_patch_path": "/path/to/pd_synth_patch.pd",
  "antescofo_external_path": "/Applications/Pd-0.56-2.app/Contents/Resources/extra/",
  "default_score_dir": "~/Music/antescofo_scores",
  "enable_logging": true,
  "log_level": "INFO"
}
```

### 2. Updated Client to Use Config

**File: `antescofo/client.py`**
- `AntescofoClient()` now reads ports from config by default
- Still accepts explicit port arguments for overrides
- Backwards compatible with existing code

### 3. Created Ready-to-Run Scripts

**File: `examples/run_demo.py`** ⭐ **START HERE**
- Complete end-to-end demo
- Generates score automatically
- Uses config system
- Shows all steps clearly
- **You will HEAR synthesized tones**

**File: `examples/setup_config.py`**
- Initialize/reset user config
- Shows current settings
- Interactive

### 4. Documentation

- **`examples/README.md`**: Comprehensive guide
- **`examples/notebook_demo.md`**: Jupyter notebook cells (with caveats)

## Quick Start Guide

### Step 1: Initialize Config

```bash
cd /Users/thorwhalen/Dropbox/py/proj/t/antescofo
python examples/setup_config.py
```

This creates `~/.config/antescofo/config.json` with your settings.

### Step 2: Setup Pure Data

1. **Open Pure Data** (Pd-0.56-2)
2. **Open**: `/Users/thorwhalen/Dropbox/py/proj/t/antescofo/antescofo/pd_synth_patch.pd`
3. **Click these message boxes** (in the patch under "- A N T E S C O F O -"):
   - `incomingosc 1`
   - `incomingoscport 5678`
   - `ascographconf localhost 9999`
   - `calibrate`
4. **Enable DSP**: Menu → Media → DSP On
5. **Leave PD running** with the patch open

### Step 3: Run the Demo

```bash
python examples/run_demo.py
```

**What happens:**
1. Script generates `simple_demo_score.asco.txt` (if not present)
2. Connects to Antescofo (running in PD)
3. Loads the score
4. Starts playback
5. **You HEAR**: C4 (440 Hz) → E4 (660 Hz) → G4 (784 Hz) tones
6. Changes tempo dynamically
7. Stops and disconnects

## Configuration Details

### View Current Config

```bash
python -c "from antescofo import print_config; print_config()"
```

### Edit Config

Edit directly: `~/.config/antescofo/config.json`

Or programmatically:
```python
from antescofo import set_config_value

set_config_value("antescofo_send_port", 6000)
set_config_value("python_receive_port", 8000)
```

### Config File Location

```
~/.config/antescofo/config.json
```

## Port Configuration Map

Understanding the port flow:

```
┌─────────────┐  Port 5678   ┌──────────────┐
│   Python    │─────────────>│  Antescofo~  │
│   Client    │              │  (in PD)     │
└─────────────┘              └──────────────┘
      ▲                              │
      │ Port 9999                    │
      └──────────────────────────────┘
      (Events back to Python)


┌─────────────┐              ┌──────────────┐
│  Antescofo  │  Port 10000  │   PD Synth   │
│  Actions    │─────────────>│  [osc~]      │
│  (OSC)      │              │  [dac~]      │
└─────────────┘              └──────────────┘
```

**In your config:**
- `antescofo_send_port: 5678` - Commands to Antescofo
- `python_receive_port: 9999` - Events from Antescofo
- `pd_listen_port: 10000` - OSC to PD synth

**In PD patch:**
- `incomingoscport 5678` - Listens for Python commands
- `ascographconf localhost 9999` - Sends events to Python
- `netreceive 10000` - Synth listens for OSC

## Notebook Usage (With Caveats)

See `examples/notebook_demo.md` for Jupyter cell examples.

**⚠️ Warning**: Notebooks may have event loop conflicts with async OSC receiving. 
**Recommended**: Use `examples/run_demo.py` script for reliable operation.

## Troubleshooting

### No Sound

1. Check PD is running with DSP ON
2. Verify you clicked the config message boxes
3. Check ports match between config and PD patch

### Connection Failed

1. Ensure PD is running
2. Ensure `antescofo~` object is loaded in PD
3. Check port numbers in config vs PD patch

### Port Already in Use

Edit `~/.config/antescofo/config.json` to use different ports, 
then update the corresponding messages in the PD patch.

## File Locations Summary

**Configuration:**
- User config: `~/.config/antescofo/config.json`
- Config module: `antescofo/util.py`

**Resources:**
- PD patch: `antescofo/pd_synth_patch.pd`
- Antescofo external: `/Applications/Pd-0.56-2.app/Contents/Resources/extra/antescofo~.pd_darwin`

**Scripts:**
- Main demo: `examples/run_demo.py` ⭐
- Config setup: `examples/setup_config.py`
- Notebook guide: `examples/notebook_demo.md`

**Generated Files:**
- Score: `simple_demo_score.asco.txt` (created by run_demo.py)

## Next Steps

1. **Run the demo**: `python examples/run_demo.py`
2. **Hear the tones** from Pure Data
3. **Experiment** with different scores
4. **Build** your own musical interactions!

Enjoy! 🎵
