"""
Basic control example for Antescofo Python interface.

This example demonstrates how to:
- Connect to an Antescofo instance
- Load a score
- Control playback (start, stop, tempo)
"""

import logging
import time
from antescofo import AntescofoClient

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)


def main():
    # Create a client (default: localhost:5678)
    client = AntescofoClient(
        host="localhost",
        port=5678,
        receive_port=None,  # Set to a port number to receive events
    )

    try:
        # Connect to Antescofo
        print("Connecting to Antescofo...")
        client.connect()

        # Load a score file
        # Replace with your actual score file path
        score_path = "path/to/your/score.asco.txt"
        print(f"Loading score: {score_path}")
        # client.load_score(score_path)

        # Start playback
        print("Starting playback...")
        client.start()

        # Wait a bit
        time.sleep(2)

        # Change tempo
        print("Setting tempo to 120 BPM")
        client.set_tempo(120)

        # Wait some more
        time.sleep(3)

        # Set tempo to 90 BPM
        print("Setting tempo to 90 BPM")
        client.set_tempo(90)

        # Wait
        time.sleep(3)

        # Stop playback
        print("Stopping playback")
        client.stop()

    finally:
        # Always disconnect when done
        print("Disconnecting...")
        client.disconnect()


# Using context manager (recommended)
def main_with_context_manager():
    """Same example using context manager."""
    with AntescofoClient() as client:
        # Load and play
        # client.load_score("path/to/score.asco.txt")
        client.start()

        # Set tempo
        client.set_tempo(120)

        # Wait for some time
        client.wait(5)

        # Stop
        client.stop()
        # Client automatically disconnects when exiting the 'with' block


if __name__ == "__main__":
    # Run the basic example
    main()

    # Or run with context manager
    # main_with_context_manager()
