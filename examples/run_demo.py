"""
Complete demo script for Antescofo with automatic configuration.

This script:
1. Generates a demo score file
2. Uses config from ~/.config/antescofo
3. Connects to Antescofo (running in Pure Data)
4. Loads and plays the score
5. Listens for events from Antescofo

PREREQUISITES:
- Pure Data is running
- The pd_synth_patch.pd is open in PD
- Antescofo external is configured (click the config messages in the patch)
- DSP is ON in PD
"""

import logging
from pathlib import Path

from antescofo import AntescofoClient, Event, EventType, ScoreBuilder
from antescofo.util import (
    get_config_value,
    resolve_score_path,
    print_config,
    init_config,
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Score file (will be created in current directory)
SCORE_NAME = "simple_demo_score.asco.txt"


def generate_demo_score(score_path: Path):
    """Generate a simple demo score with synth actions."""
    print(f"\n[SETUP] Generating score: {score_path}")

    builder = (
        ScoreBuilder()
        .comment("Simple Demo Score with PD Synth")
        .raw("@global $volume := 0.5")
        .raw("@global $pd_port := 10000")
        .raw("")
        .comment("=== NOTE 1: Play C4 (440 Hz) ===")
        .event("NOTE", 1.0, "C4 60")
        .action('OSC "/synth/play" 440 $volume')
        .action('print "▶ Playing C4 at 440Hz"')
        .raw("")
        .comment("=== NOTE 2: Play E4 (660 Hz) ===")
        .event("NOTE", 1.0, "E4 64")
        .action('OSC "/synth/play" 660 $volume')
        .action('print "▶ Playing E4 at 660Hz"')
        .raw("")
        .comment("=== NOTE 3: Play G4 (784 Hz) ===")
        .event("NOTE", 1.0, "G4 67")
        .action('OSC "/synth/play" 784 $volume')
        .action('print "▶ Playing G4 at 784Hz"')
        .raw("")
        .comment("=== END: Stop synth ===")
        .event("NOTE", 0.5, "C5 72")
        .action('OSC "/synth/stop" 0')
        .action('print "⏹ Score finished - synth stopped"')
    )

    builder.save(score_path)
    print(f"[SETUP] ✓ Score generated at {score_path}")


def on_action_trace(event: Event):
    """Handle action execution messages from Antescofo."""
    if isinstance(event.data, tuple) and len(event.data) > 5:
        # Action trace format: (name, type, father, now, rnow, message)
        action_type = event.data[1].upper()
        message = event.data[5]
        print(f"  [{action_type}] {message}")
    else:
        print(f"  [TRACE] {event.data}")


def on_tempo_change(event: Event):
    """Handle tempo changes from Antescofo."""
    print(f"  [TEMPO] Changed to {event.data} BPM")


def main():
    """Run the complete Antescofo demo."""
    print("\n" + "=" * 70)
    print("        ANTESCOFO / PUREDATA OSC DEMO")
    print("=" * 70)

    # Show current configuration
    print("\n[CONFIG] Current settings:")
    config = {
        "antescofo_send_port": get_config_value("antescofo_send_port"),
        "python_receive_port": get_config_value("python_receive_port"),
        "pd_listen_port": get_config_value("pd_listen_port"),
    }
    for key, value in config.items():
        print(f"  {key}: {value}")

    print(f"\n  Config file: ~/.config/antescofo/config.json")
    print(
        f"  (Run 'python -c \"from antescofo.util import print_config; print_config()\"' to see all settings)"
    )

    # Generate score
    score_path = Path(SCORE_NAME)
    if not score_path.exists():
        generate_demo_score(score_path)
    else:
        print(f"\n[SETUP] Using existing score: {score_path}")

    # Verify PD setup
    print("\n" + "-" * 70)
    print("PREREQUISITES CHECK:")
    print("  ✓ Score file created")
    print("  ? Pure Data running with pd_synth_patch.pd open?")
    print("  ? Antescofo external configured (click config messages)?")
    print("  ? DSP enabled in PD (Media → DSP On)?")
    print("-" * 70)

    input("\nPress ENTER when Pure Data is ready...")

    # Create client (uses config automatically)
    print("\n[CONNECT] Creating Antescofo client...")
    client = AntescofoClient()

    try:
        # Connect
        print("[CONNECT] Connecting to Antescofo...")
        client.connect()
        print(f"[CONNECT] ✓ Connected to {client.host}:{client.port}")
        print(f"[CONNECT] ✓ Listening for events on port {client.receive_port}")

        # Subscribe to events
        print("\n[EVENTS] Subscribing to Antescofo events...")
        client.on(EventType.ACTION_TRACE, on_action_trace)
        client.on(EventType.TEMPO, on_tempo_change)
        print("[EVENTS] ✓ Event handlers registered")

        # Load score
        print(f"\n[LOAD] Loading score: {score_path.name}")
        client.load_score(score_path.resolve())
        print("[LOAD] ✓ Score loaded into Antescofo")

        # Start playback
        print("\n[PLAY] Starting score playback...")
        print("-" * 70)
        print("🎵 LISTEN: You should hear tones from Pure Data now...")
        print("-" * 70)
        client.start()

        # Dynamic tempo change
        client.wait(2.5)
        print("\n[CONTROL] Changing tempo to 150 BPM...")
        client.set_tempo(150.0)

        # Wait for score to complete
        print("\n[WAIT] Waiting for score to finish (5 seconds)...")
        client.wait(5)

        # Stop
        print("\n[STOP] Stopping playback...")
        client.stop()

        print("\n" + "=" * 70)
        print("✓ DEMO COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTROUBLESHOOTING:")
        print("  1. Is Pure Data running?")
        print("  2. Is pd_synth_patch.pd open?")
        print("  3. Did you click the Antescofo config messages in the patch?")
        print("  4. Are the ports correct in your config?")
        print(f"     - Antescofo listening on: {get_config_value('antescofo_send_port')}")
        print(f"     - Python listening on: {get_config_value('python_receive_port')}")
        print(f"     - PD synth listening on: {get_config_value('pd_listen_port')}")

    finally:
        client.disconnect()
        print("\n[DISCONNECT] Client disconnected.\n")


if __name__ == "__main__":
    # Initialize config on first run
    init_config()

    # Run demo
    main()
