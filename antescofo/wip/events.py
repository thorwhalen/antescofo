"""
Event representation for score playback.

This module defines the Event data structure used by the SimpleScorePlayer.
"""

from dataclasses import dataclass, field


@dataclass
class Event:
    """A musical event in a score.

    Represents a single event (note, chord, etc.) with associated actions.

    Attributes:
        type: Event type (e.g., "NOTE", "CHORD")
        duration: Duration in beats
        data: Event-specific data (e.g., "C4 60" for MIDI note)
        actions: List of actions to execute when event triggers

    Example:
        >>> event = Event("NOTE", 1.0, "C4 60", ['print "Hello"'])
        >>> event.type
        'NOTE'
        >>> event.duration
        1.0
    """

    type: str
    duration: float
    data: str
    actions: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        actions_str = f", {len(self.actions)} actions" if self.actions else ""
        return f"Event({self.type}, {self.duration}s, {self.data!r}{actions_str})"
