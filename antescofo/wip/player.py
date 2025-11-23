"""
Simple score player - Python-native alternative to Antescofo playback.

This module provides a lightweight score playback engine that doesn't require
Max/MSP, PureData, or external Antescofo installation. It focuses on timing
and event triggering, delegating sound synthesis to callbacks.
"""

import time
from typing import Callable, Iterator, Optional
from collections.abc import Iterable

from .events import Event


class SimpleScorePlayer:
    """Play Antescofo-style scores using Python callbacks.

    This is a lightweight alternative that doesn't require Max/MSP or PureData.
    Focuses on timing and event triggering, delegates sound synthesis to callbacks.

    Attributes:
        score: List of Event objects to play
        tempo: Playback tempo in beats per minute
        sound_callback: Function called for each note event
        action_callback: Function called for each action

    Example:
        >>> from antescofo.wip import Event, SimpleScorePlayer
        >>> events = [
        ...     Event("NOTE", 1.0, "C4 60", ['print "C4"']),
        ...     Event("NOTE", 1.0, "D4 62", ['print "D4"']),
        ... ]
        >>> player = SimpleScorePlayer(events, tempo=120)
        >>> # player.play()  # Would play in real-time
    """

    def __init__(
        self,
        score: Iterable[Event],
        *,
        tempo: float = 120,
        sound_callback: Optional[Callable[[Event], None]] = None,
        action_callback: Optional[Callable[[str], None]] = None,
    ):
        """Initialize player.

        Args:
            score: Iterable of Event objects
            tempo: Beats per minute (default: 120)
            sound_callback: Function called for each note event.
                           If None, uses default print handler.
            action_callback: Function called for each action.
                            If None, uses default print handler.
        """
        self.score = list(score)
        self.tempo = tempo
        self.sound_callback = sound_callback or self._default_sound
        self.action_callback = action_callback or self._default_action

    def _beat_to_seconds(self, beats: float) -> float:
        """Convert beat duration to seconds based on tempo.

        Args:
            beats: Duration in beats

        Returns:
            Duration in seconds
        """
        return (beats * 60.0) / self.tempo

    def _default_sound(self, event: Event) -> None:
        """Default sound handler - just prints event info.

        Args:
            event: The event to handle
        """
        print(f"🎵 {event.type}: {event.data}")

    def _default_action(self, action: str) -> None:
        """Default action handler - just prints action code.

        Args:
            action: The action code to execute
        """
        print(f"⚡ Action: {action}")

    def play(self) -> None:
        """Play the score in real-time.

        Iterates through events, triggers callbacks, and sleeps for correct duration.
        This is a blocking operation that runs until the score completes.
        """
        print(f"▶️  Playing score at {self.tempo} BPM...")

        for event in self.score:
            # Trigger sound
            self.sound_callback(event)

            # Execute actions
            for action in event.actions:
                self.action_callback(action)

            # Wait for event duration
            duration_seconds = self._beat_to_seconds(event.duration)
            time.sleep(duration_seconds)

        print("✅ Playback complete")

    def events(self) -> Iterator[tuple[float, Event]]:
        """Yield (timestamp, event) pairs for external scheduling.

        Useful for integrating with other timing systems or for non-blocking playback.

        Yields:
            Tuples of (absolute_time_seconds, event)

        Example:
            >>> from antescofo.wip import Event, SimpleScorePlayer
            >>> events = [Event("NOTE", 1.0, "C4 60")]
            >>> player = SimpleScorePlayer(events, tempo=120)
            >>> list(player.events())  # doctest: +ELLIPSIS
            [(0.0, Event(NOTE, 1.0s, 'C4 60'))]
        """
        current_time = 0.0
        for event in self.score:
            yield (current_time, event)
            current_time += self._beat_to_seconds(event.duration)

    def set_tempo(self, tempo: float) -> None:
        """Change the playback tempo.

        Args:
            tempo: New tempo in beats per minute
        """
        self.tempo = tempo
        print(f"🎵 Tempo set to: {tempo} BPM")
