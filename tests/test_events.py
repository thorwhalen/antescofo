"""Tests for event handling."""

import pytest
from antescofo import Event, EventType, ActionTraceEvent, EventDispatcher


class TestEventType:
    """Tests for EventType enum."""

    def test_from_message_known(self):
        """Test converting known message types."""
        assert EventType.from_message("tempo") == EventType.TEMPO
        assert EventType.from_message("stop") == EventType.STOP
        assert EventType.from_message("event_beatpos") == EventType.BEAT_POSITION

    def test_from_message_unknown(self):
        """Test converting unknown message types."""
        assert EventType.from_message("unknown_type") == EventType.UNKNOWN


class TestEvent:
    """Tests for the Event class."""

    def test_create_event(self):
        """Test creating an event."""
        event = Event(EventType.TEMPO, 120.0)
        assert event.event_type == EventType.TEMPO
        assert event.data == 120.0

    def test_event_with_address(self):
        """Test creating an event with raw address."""
        event = Event(EventType.TEMPO, 120.0, raw_address="/antescofo/tempo")
        assert event.raw_address == "/antescofo/tempo"


class TestActionTraceEvent:
    """Tests for ActionTraceEvent."""

    def test_create_action_trace(self):
        """Test creating an action trace event."""
        event = ActionTraceEvent(
            action_name="my_action",
            trace_type="message",
            father_name="parent",
            now=10.5,
            rnow=2.3,
            message="test message",
        )
        assert event.action_name == "my_action"
        assert event.trace_type == "message"
        assert event.father_name == "parent"
        assert event.now == 10.5
        assert event.rnow == 2.3
        assert event.message == "test message"
        assert event.event_type == EventType.ACTION_TRACE


class TestEventDispatcher:
    """Tests for EventDispatcher."""

    def test_create_dispatcher(self):
        """Test creating a dispatcher."""
        dispatcher = EventDispatcher()
        assert dispatcher is not None

    def test_subscribe_and_dispatch(self):
        """Test subscribing and dispatching events."""
        dispatcher = EventDispatcher()
        received = []

        def handler(event):
            received.append(event)

        # Subscribe to tempo events
        dispatcher.subscribe(EventType.TEMPO, handler)

        # Dispatch a tempo event
        event = Event(EventType.TEMPO, 120.0)
        dispatcher.dispatch(event)

        # Check it was received
        assert len(received) == 1
        assert received[0] == event

    def test_subscribe_to_all_events(self):
        """Test subscribing to all events."""
        dispatcher = EventDispatcher()
        received = []

        def handler(event):
            received.append(event)

        # Subscribe to all events
        dispatcher.subscribe(None, handler)

        # Dispatch different events
        dispatcher.dispatch(Event(EventType.TEMPO, 120.0))
        dispatcher.dispatch(Event(EventType.STOP, None))

        # Check both were received
        assert len(received) == 2

    def test_multiple_handlers(self):
        """Test multiple handlers for same event type."""
        dispatcher = EventDispatcher()
        received1 = []
        received2 = []

        def handler1(event):
            received1.append(event)

        def handler2(event):
            received2.append(event)

        # Subscribe both handlers
        dispatcher.subscribe(EventType.TEMPO, handler1)
        dispatcher.subscribe(EventType.TEMPO, handler2)

        # Dispatch event
        event = Event(EventType.TEMPO, 120.0)
        dispatcher.dispatch(event)

        # Both should receive it
        assert len(received1) == 1
        assert len(received2) == 1

    def test_unsubscribe(self):
        """Test unsubscribing from events."""
        dispatcher = EventDispatcher()
        received = []

        def handler(event):
            received.append(event)

        # Subscribe and then unsubscribe
        dispatcher.subscribe(EventType.TEMPO, handler)
        dispatcher.unsubscribe(EventType.TEMPO, handler)

        # Dispatch event
        dispatcher.dispatch(Event(EventType.TEMPO, 120.0))

        # Should not be received
        assert len(received) == 0

    def test_clear(self):
        """Test clearing all handlers."""
        dispatcher = EventDispatcher()
        received = []

        def handler(event):
            received.append(event)

        # Subscribe
        dispatcher.subscribe(EventType.TEMPO, handler)

        # Clear all handlers
        dispatcher.clear()

        # Dispatch event
        dispatcher.dispatch(Event(EventType.TEMPO, 120.0))

        # Should not be received
        assert len(received) == 0

    def test_handler_exception_handling(self):
        """Test that exceptions in handlers don't break dispatching."""
        dispatcher = EventDispatcher()
        received = []

        def bad_handler(event):
            raise ValueError("Handler error")

        def good_handler(event):
            received.append(event)

        # Subscribe both handlers
        dispatcher.subscribe(EventType.TEMPO, bad_handler)
        dispatcher.subscribe(EventType.TEMPO, good_handler)

        # Dispatch event - should not raise
        event = Event(EventType.TEMPO, 120.0)
        dispatcher.dispatch(event)

        # Good handler should still receive the event
        assert len(received) == 1
