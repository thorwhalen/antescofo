"""
Event listening example for Antescofo Python interface.

This example demonstrates how to:
- Subscribe to events from Antescofo
- Handle different event types
- React to tempo changes, beat positions, etc.
"""

import logging
import time
from antescofo import AntescofoClient, Event, EventType, ActionTraceEvent

# Enable logging
logging.basicConfig(level=logging.INFO)


def on_tempo_change(event: Event):
    """Called when tempo changes."""
    print(f"Tempo changed to: {event.data}")


def on_beat_position(event: Event):
    """Called when beat position updates."""
    print(f"Beat position: {event.data}")


def on_action_trace(event: ActionTraceEvent):
    """Called when an action is traced."""
    print(
        f"Action traced: {event.action_name} ({event.trace_type}) "
        f"at {event.rnow} - {event.message}"
    )


def on_any_event(event: Event):
    """Called for any event."""
    print(f"Received event: {event.event_type.value}")


def main():
    # Create client with a receive port to get events
    client = AntescofoClient(
        host="localhost",
        port=5678,
        receive_port=9999,  # Port to receive events on
    )

    try:
        # Connect
        print("Connecting to Antescofo...")
        client.connect()

        # Subscribe to specific events
        print("Subscribing to events...")
        client.on(EventType.TEMPO, on_tempo_change)
        client.on(EventType.BEAT_POSITION, on_beat_position)
        client.on(EventType.ACTION_TRACE, on_action_trace)

        # Subscribe to all events
        # client.on(None, on_any_event)

        # Or subscribe using string names
        # client.on("tempo", on_tempo_change)

        # Load and play
        print("Loading score and starting playback...")
        # client.load_score("path/to/score.asco.txt")
        client.start()

        # Keep running to receive events
        print("Listening for events... (press Ctrl+C to stop)")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopping...")

        # Stop playback
        client.stop()

    finally:
        print("Disconnecting...")
        client.disconnect()


# Alternative: Using lambda functions
def main_with_lambdas():
    """Example using lambda functions for event handlers."""
    with AntescofoClient(receive_port=9999) as client:
        # Subscribe with lambdas
        client.on(EventType.TEMPO, lambda e: print(f"Tempo: {e.data}"))
        client.on(EventType.BEAT_POSITION, lambda e: print(f"Beat: {e.data}"))

        # Start and listen
        client.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

        client.stop()


if __name__ == "__main__":
    main()
    # main_with_lambdas()
