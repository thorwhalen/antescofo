"""
Utility script to generate a simple Antescofo score file for the demo.

The score defines two notes and three actions:
1. When NOTE_1 is detected (or time passes), send an OSC message to PD synth.
2. When NOTE_2 is detected, change the global tempo variable.
3. The PD patch will be listening for '/synth/play' and react accordingly.
"""

from antescofo import ScoreBuilder
from pathlib import Path

# Define the score file path relative to the root directory
SCORE_FILE = Path("simple_demo_score.asco.txt")


def generate_score():
    """Generates a simple, playable Antescofo score."""
    builder = (
        ScoreBuilder()
        .comment("Simple Score for Python/PD OSC Demo")
        .raw("@global $volume := 0.5")  # Define a variable
        .raw("@global $pitch_offset := 0")  # Define a variable
        .raw("")
        .comment("--- NOTE 1 ---")
        .event("NOTE", 1.0, "C4 60")  # Event type, duration in beats, midi pitch
        .action('OSC "/synth/play" 440 $volume')  # Action 1: Send OSC message to PD
        .action('print "Action 1 triggered: playing C4"')
        .comment("--- NOTE 2 ---")
        .event("NOTE", 1.0, "E4 64")
        .action('OSC "/synth/play" 660 $volume')  # Action 2: Send OSC message to PD (higher pitch)
        .action('print "Action 2 triggered: playing E4"')
        .comment("--- NOTE 3 ---")
        .event("NOTE", 0.5, "G4 67")
        .action('print "Score finished."')  # Final action
        .action('OSC "/synth/stop" 0')  # Stop the synth
    )

    builder.save(SCORE_FILE)
    print(f"\n[INFO] Generated Antescofo score file: {SCORE_FILE.resolve()}")


if __name__ == "__main__":
    # Ensure the required dependencies (like ScoreBuilder) are available
    try:
        generate_score()
    except ImportError:
        print("\n[ERROR] Could not run score_generator.py.")
        print("Please ensure your antescofo package structure is installed correctly.")
        print("Required Python dependency: python-osc (part of the antescofo package)")
