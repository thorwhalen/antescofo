"""
Score builder for creating playable scores.

This module provides an enhanced ScoreBuilder that works with both:
- The original Antescofo text format (for OSC client)
- The SimpleScorePlayer (for direct Python playback)
"""

from typing import Iterator
from pathlib import Path

from .events import Event


class PlayableScoreBuilder:
    """Build Antescofo scores that can be played directly in Python.

    This builder creates both:
    1. Antescofo text format (for saving .asco files)
    2. Event objects (for SimpleScorePlayer)

    Can be used as a drop-in replacement for the original ScoreBuilder
    while adding playback capabilities.

    Example:
        >>> builder = (
        ...     PlayableScoreBuilder()
        ...     .comment("C Major Scale")
        ...     .event("NOTE", 1.0, "C4 60")
        ...     .action('print "C4"')
        ...     .event("NOTE", 1.0, "D4 62")
        ... )
        >>> events = builder.build()
        >>> len(events)
        2
        >>> str(builder).split('\\n')[0]
        '; C Major Scale'
    """

    def __init__(self):
        """Initialize an empty score builder."""
        self._lines: list[str] = []
        self._events: list[Event] = []
        self._current_actions: list[str] = []

    def comment(self, text: str) -> 'PlayableScoreBuilder':
        """Add a comment line.

        Args:
            text: Comment text (will be prefixed with ';')

        Returns:
            Self for method chaining
        """
        self._lines.append(f"; {text}")
        return self

    def raw(self, line: str) -> 'PlayableScoreBuilder':
        """Add a raw Antescofo script line.

        Args:
            line: Raw line to add (variable definitions, functions, etc.)

        Returns:
            Self for method chaining
        """
        self._lines.append(line)
        return self

    def event(
        self,
        event_type: str,
        duration: float,
        data: str,
    ) -> 'PlayableScoreBuilder':
        """Add an event (note, chord, etc.).

        Args:
            event_type: Type of event (e.g., "NOTE", "CHORD")
            duration: Duration in beats
            data: Event data (e.g., "C4 60" for MIDI note)

        Returns:
            Self for method chaining
        """
        # Save previous event's actions
        if self._current_actions and self._events:
            self._events[-1].actions.extend(self._current_actions)
            self._current_actions = []

        # Add to text representation
        self._lines.append(f"{event_type} {duration} {data}")

        # Add to event list
        event_obj = Event(event_type, duration, data, [])
        self._events.append(event_obj)

        return self

    def action(self, code: str) -> 'PlayableScoreBuilder':
        """Add an action to the last event.

        Args:
            code: Antescofo action code to execute

        Returns:
            Self for method chaining
        """
        self._lines.append(f"    {code}")
        self._current_actions.append(code)
        return self

    def build(self) -> list[Event]:
        """Build and return the list of Event objects for playback.

        Finalizes the score and returns Event objects ready for SimpleScorePlayer.

        Returns:
            List of Event objects
        """
        # Finalize last event's actions
        if self._current_actions and self._events:
            self._events[-1].actions.extend(self._current_actions)
            self._current_actions = []
        return self._events.copy()

    def __iter__(self) -> Iterator[Event]:
        """Make builder directly iterable.

        Allows using the builder directly with SimpleScorePlayer:
            player = SimpleScorePlayer(builder, tempo=120)
        """
        yield from self.build()

    def __str__(self) -> str:
        """Return Antescofo script text representation.

        Returns:
            Complete Antescofo script as string
        """
        return "\n".join(self._lines)

    def save(self, filepath: str | Path) -> None:
        """Save score to Antescofo text file.

        Args:
            filepath: Path to save the .asco.txt file
        """
        filepath = Path(filepath)
        filepath.write_text(str(self), encoding="utf-8")
        print(f"✅ Saved score to: {filepath}")

    def get_text(self) -> str:
        """Get the Antescofo script text.

        Alias for __str__() for clarity.

        Returns:
            Complete Antescofo script as string
        """
        return str(self)
