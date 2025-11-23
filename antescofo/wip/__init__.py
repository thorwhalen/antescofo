"""
WIP (Work In Progress) - Python-native Antescofo alternative.

This package provides a lightweight, Python-only implementation for testing
and experimentation without requiring Max/MSP, PureData, or external Antescofo.

Use this for:
- Development and testing
- Simple playback scenarios
- Apple Silicon compatibility
- Learning and experimentation

Use the main antescofo package (client.py) for:
- Connecting to real Antescofo instances
- Score following (live musician tracking)
- Production performances

Basic usage:
    >>> from antescofo.wip import PlayableScoreBuilder, SimpleScorePlayer
    >>>
    >>> # Build a score
    >>> score = (
    ...     PlayableScoreBuilder()
    ...     .comment("Simple melody")
    ...     .event("NOTE", 1.0, "C4 60")
    ...     .event("NOTE", 1.0, "D4 62")
    ...     .event("NOTE", 1.0, "E4 64")
    ... )
    >>>
    >>> # Play it (prints events by default)
    >>> player = SimpleScorePlayer(score, tempo=120)
    >>> # player.play()  # Uncomment to play

Audio playback:
    >>> from antescofo.wip import play_with_audio, play_with_midi
    >>> # play_with_audio(score)  # Requires: pip install sounddevice numpy
    >>> # play_with_midi(score)   # Requires: pip install python-rtmidi mido
"""

from .events import Event
from .player import SimpleScorePlayer
from .audio import play_with_audio, play_with_midi, create_custom_player
from .builder import PlayableScoreBuilder

__all__ = [
    'Event',
    'SimpleScorePlayer',
    'PlayableScoreBuilder',
    'play_with_audio',
    'play_with_midi',
    'create_custom_player',
]
