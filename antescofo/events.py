"""
Event handling system for Antescofo.

Provides a way to subscribe to and handle events from Antescofo,
such as beat position changes, tempo changes, action traces, etc.
"""

from typing import Any, Callable, Dict, List, Optional
from enum import Enum
import logging

from .constants import (
    MSG_STOP,
    MSG_EVENT_BEATPOS,
    MSG_RNOW,
    MSG_TEMPO,
    MSG_PITCH,
    MSG_ACTION_TRACE,
    MSG_LOAD_SCORE,
)


logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events that can be received from Antescofo."""

    STOP = "stop"
    BEAT_POSITION = "event_beatpos"
    RNOW = "rnow"
    TEMPO = "tempo"
    PITCH = "pitch"
    ACTION_TRACE = "action_trace"
    LOAD_SCORE = "loadscore"
    UNKNOWN = "unknown"

    @classmethod
    def from_message(cls, message_type: str) -> "EventType":
        """Get EventType from message type string."""
        for event_type in cls:
            if event_type.value == message_type:
                return event_type
        return cls.UNKNOWN


class Event:
    """Represents an event received from Antescofo."""

    def __init__(self, event_type: EventType, data: Any, raw_address: str = None):
        """
        Initialize an Event.

        Args:
            event_type: Type of the event
            data: Event data (can be a single value or list of values)
            raw_address: The raw OSC address pattern
        """
        self.event_type = event_type
        self.data = data
        self.raw_address = raw_address

    def __repr__(self) -> str:
        return f"Event(type={self.event_type}, data={self.data})"


class ActionTraceEvent(Event):
    """Specialized event for action traces."""

    def __init__(
        self,
        action_name: str,
        trace_type: str,
        father_name: str,
        now: float,
        rnow: float,
        message: str,
        raw_address: str = None,
    ):
        """
        Initialize an ActionTraceEvent.

        Args:
            action_name: Name of the action
            trace_type: Type of trace (message, abort, assignment, etc.)
            father_name: Name of the parent action
            now: Absolute time
            rnow: Relative time
            message: Trace message
            raw_address: The raw OSC address pattern
        """
        super().__init__(EventType.ACTION_TRACE, None, raw_address)
        self.action_name = action_name
        self.trace_type = trace_type
        self.father_name = father_name
        self.now = now
        self.rnow = rnow
        self.message = message

    def __repr__(self) -> str:
        return (
            f"ActionTraceEvent(action={self.action_name}, type={self.trace_type}, "
            f"now={self.now}, rnow={self.rnow})"
        )


# Type for event handlers
EventHandler = Callable[[Event], None]


class EventDispatcher:
    """
    Manages event subscriptions and dispatching.

    Allows subscribing to specific event types and dispatching events
    to registered handlers.
    """

    def __init__(self):
        """Initialize the EventDispatcher."""
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []

    def subscribe(
        self, event_type: Optional[EventType], handler: EventHandler
    ) -> None:
        """
        Subscribe to an event type.

        Args:
            event_type: Type of event to subscribe to, or None for all events
            handler: Callback function to handle the event
        """
        if event_type is None:
            self._global_handlers.append(handler)
        else:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(handler)
        logger.debug(f"Subscribed handler to {event_type}")

    def unsubscribe(
        self, event_type: Optional[EventType], handler: EventHandler
    ) -> None:
        """
        Unsubscribe from an event type.

        Args:
            event_type: Type of event to unsubscribe from, or None for global handlers
            handler: Handler to remove
        """
        if event_type is None:
            if handler in self._global_handlers:
                self._global_handlers.remove(handler)
        else:
            if event_type in self._handlers and handler in self._handlers[event_type]:
                self._handlers[event_type].remove(handler)
        logger.debug(f"Unsubscribed handler from {event_type}")

    def dispatch(self, event: Event) -> None:
        """
        Dispatch an event to all registered handlers.

        Args:
            event: Event to dispatch
        """
        logger.debug(f"Dispatching event: {event}")

        # Call global handlers
        for handler in self._global_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in global event handler: {e}", exc_info=True)

        # Call specific handlers
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(
                        f"Error in event handler for {event.event_type}: {e}",
                        exc_info=True,
                    )

    def clear(self) -> None:
        """Clear all event handlers."""
        self._handlers.clear()
        self._global_handlers.clear()
        logger.debug("Cleared all event handlers")
