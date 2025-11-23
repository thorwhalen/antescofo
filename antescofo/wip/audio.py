"""
Audio playback backends for SimpleScorePlayer.

This module provides various audio output options:
- MIDI output
- Synthesized audio (sine waves)
- External synthesis hooks

Each function creates a SimpleScorePlayer configured with the appropriate callbacks.
"""

from typing import Optional
from collections.abc import Iterable

from .events import Event
from .player import SimpleScorePlayer


def play_with_midi(
    score: Iterable[Event],
    *,
    tempo: float = 120,
    port_name: Optional[str] = None,
) -> None:
    """Play score using MIDI output.

    Requires: pip install python-rtmidi mido

    Args:
        score: Iterable of Event objects
        tempo: Playback tempo in BPM
        port_name: Name of MIDI port to use (None for default)

    Example:
        >>> from antescofo.wip import Event, play_with_midi
        >>> score = [Event("NOTE", 1.0, "C4 60")]
        >>> # play_with_midi(score)  # Would play via MIDI
    """
    try:
        import mido
        from mido import Message
    except ImportError as e:
        raise ImportError("MIDI playback requires: pip install python-rtmidi mido") from e

    # Open MIDI output
    if port_name:
        port = mido.open_output(port_name)
    else:
        port = mido.open_output()

    def _send_note(event: Event) -> None:
        """Parse and send MIDI note."""
        parts = event.data.split()
        if len(parts) >= 2:
            # Extract MIDI note number (e.g., "C4 60" → 60)
            midi_note = int(parts[1])
            velocity = 64  # Default velocity

            # Send note on
            port.send(Message('note_on', note=midi_note, velocity=velocity))
            print(f"🎹 MIDI Note: {midi_note} (velocity {velocity})")

    def _send_note_off(event: Event) -> None:
        """Send note off after duration."""
        parts = event.data.split()
        if len(parts) >= 2:
            midi_note = int(parts[1])
            port.send(Message('note_off', note=midi_note))

    try:
        player = SimpleScorePlayer(
            score,
            tempo=tempo,
            sound_callback=_send_note,
        )
        player.play()
    finally:
        # Send all notes off and close port
        port.send(Message('control_change', control=123, value=0))  # All notes off
        port.close()


def play_with_audio(
    score: Iterable[Event],
    *,
    tempo: float = 120,
    sample_rate: int = 44100,
    volume: float = 0.3,
) -> None:
    """Play score with simple synthesized audio.

    Uses sine wave synthesis for a basic but functional audio output.
    Requires: pip install sounddevice numpy

    Args:
        score: Iterable of Event objects
        tempo: Playback tempo in BPM
        sample_rate: Audio sample rate in Hz
        volume: Playback volume (0.0 to 1.0)

    Example:
        >>> from antescofo.wip import Event, play_with_audio
        >>> score = [Event("NOTE", 1.0, "C4 60")]
        >>> # play_with_audio(score)  # Would play synthesized audio
    """
    try:
        import sounddevice as sd
        import numpy as np
    except ImportError as e:
        raise ImportError("Audio playback requires: pip install sounddevice numpy") from e

    def _note_to_freq(midi_note: int) -> float:
        """Convert MIDI note number to frequency in Hz.

        Uses standard MIDI tuning: A4 (MIDI 69) = 440 Hz
        """
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

    def _play_tone(event: Event) -> None:
        """Generate and play a simple sine wave tone."""
        parts = event.data.split()
        if len(parts) >= 2:
            midi_note = int(parts[1])
            freq = _note_to_freq(midi_note)
            duration = (event.duration * 60.0) / tempo

            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = volume * np.sin(2 * np.pi * freq * t)

            # Apply simple envelope (fade in/out to avoid clicks)
            envelope = np.ones_like(wave)
            fade_samples = int(0.01 * sample_rate)  # 10ms fade
            if len(envelope) > 2 * fade_samples:
                envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

            print(f"🔊 Playing: {freq:.1f} Hz ({midi_note}) for {duration:.2f}s")

            # Play audio (blocking)
            sd.play(wave * envelope, sample_rate)
            sd.wait()

    player = SimpleScorePlayer(
        score,
        tempo=tempo,
        sound_callback=_play_tone,
    )
    player.play()


def create_custom_player(
    score: Iterable[Event],
    *,
    tempo: float = 120,
    on_note: Optional[callable] = None,
    on_action: Optional[callable] = None,
) -> SimpleScorePlayer:
    """Create a player with custom callbacks.

    Use this to integrate with your own synthesis or control systems.

    Args:
        score: Iterable of Event objects
        tempo: Playback tempo in BPM
        on_note: Callback for note events (receives Event object)
        on_action: Callback for actions (receives action string)

    Returns:
        Configured SimpleScorePlayer instance

    Example:
        >>> from antescofo.wip import Event, create_custom_player
        >>> def my_synth(event):
        ...     print(f"Custom synth: {event.data}")
        >>> score = [Event("NOTE", 1.0, "C4 60")]
        >>> player = create_custom_player(score, on_note=my_synth)
        >>> # player.play()  # Would use custom callback
    """
    return SimpleScorePlayer(
        score,
        tempo=tempo,
        sound_callback=on_note,
        action_callback=on_action,
    )
