"""
High-level client interface for Antescofo.

Provides a user-friendly API for controlling Antescofo instances.
"""

import logging
import time
from pathlib import Path
from typing import Any, Callable, Optional, Union

from .constants import (
    CMD_ASCOGRAPHCOMM,
    CMD_ASCOGRAPHCONF,
    CMD_INCOMINGOSC,
    CMD_INCOMING_OSC_PORT,
    CMD_LOAD,
    CMD_NEXTEVENT,
    CMD_PAUSE,
    CMD_PREVEVENT,
    CMD_RESUME,
    CMD_START,
    CMD_STOP,
    CMD_TEMPO,
    DEFAULT_ANTESCOFO_PORT,
    DEFAULT_ASCOGRAPH_PORT,
    DEFAULT_HOST,
    OSC_PREFIX_ANTESCOFO,
)
from .events import Event, EventType
from .exceptions import AntescofoException, ConnectionError
from .osc import OSCCommunicator
from .types import AntescofoValue, to_osc_value
from .util import get_config_value

logger = logging.getLogger(__name__)


class AntescofoClient:
    """
    High-level client for controlling an Antescofo instance.

    This class provides a Pythonic interface to Antescofo, allowing you to:
    - Load and control score playback
    - Send OSC messages
    - Subscribe to events
    - Control transport (start, stop, tempo, etc.)

    Example:
        >>> client = AntescofoClient()
        >>> client.connect()
        >>> client.load_score("myscore.asco.txt")
        >>> client.start()
        >>> client.set_tempo(120)
        >>> client.stop()
        >>> client.disconnect()

    Or use as a context manager:
        >>> with AntescofoClient() as client:
        ...     client.load_score("myscore.asco.txt")
        ...     client.start()
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = None,
        receive_port: Optional[int] = None,
        auto_connect: bool = False,
    ):
        """
        Initialize the Antescofo client.

        Args:
            host: Hostname or IP of the Antescofo instance (default: localhost)
            port: Port to send messages to (default: from config or 5678)
            receive_port: Port to receive messages on (default: from config or None)
            auto_connect: Whether to automatically connect on initialization
        """
        self.host = host
        self.port = (
            port
            if port is not None
            else get_config_value("antescofo_send_port", DEFAULT_ANTESCOFO_PORT)
        )
        self.receive_port = (
            receive_port
            if receive_port is not None
            else get_config_value("python_receive_port", None)
        )

        self._osc: Optional[OSCCommunicator] = None
        self._connected = False

        if auto_connect:
            self.connect()

    def connect(self):
        """
        Establish connection to Antescofo.

        Creates the OSC communicator and starts receiving if a receive port is configured.
        """
        if self._connected:
            logger.warning("Already connected to Antescofo")
            return

        try:
            self._osc = OSCCommunicator(self.host, self.port, self.receive_port)
            self._connected = True  # Set connected before calling other methods

            # Start receiving if enabled
            if self.receive_port is not None:
                self._osc.start_receiving()
                # Enable OSC communication in Antescofo
                self.enable_osc_communication()

            logger.info(f"Connected to Antescofo at {self.host}:{self.port}")

        except Exception as e:
            self._connected = False  # Reset on failure
            if self._osc:
                self._osc.close()
                self._osc = None
            raise ConnectionError(
                f"Failed to connect to Antescofo at {self.host}:{self.port}: {e}\n\n"
                f"Make sure Antescofo is running and listening on {self.host}:{self.port}.\n"
                f"You need to have Antescofo (Max/MSP external, PureData external, or standalone) "
                f"running before you can use this Python client.\n\n"
                f"To check if Antescofo is running:\n"
                f"  - If using Max/MSP: Check that the antescofo~ object is loaded\n"
                f"  - If using PureData: Check that the antescofo external is loaded\n"
                f"  - If using standalone: Launch the Antescofo application\n\n"
                f"For more information, see: https://antescofo-doc.ircam.fr/"
            )

    def disconnect(self):
        """
        Disconnect from Antescofo.

        Stops receiving and cleans up resources.
        """
        if not self._connected:
            return

        if self._osc:
            self._osc.close()
            self._osc = None

        self._connected = False
        logger.info("Disconnected from Antescofo")

    def _ensure_connected(self):
        """Ensure we're connected to Antescofo."""
        if not self._connected or self._osc is None:
            raise AntescofoException("Not connected to Antescofo. Call connect() first.")

    def _send_command(self, command: str, *args):
        """
        Send an internal command to Antescofo.

        Args:
            command: Command name
            *args: Command arguments
        """
        self._ensure_connected()
        # Commands are sent as raw messages (not via OSC address)
        self._osc.send_raw(command, *args)

    def send_osc(self, address: str, *args):
        """
        Send an OSC message to Antescofo.

        Args:
            address: OSC address (will be prefixed with /antescofo/ if not present)
            *args: Message arguments
        """
        self._ensure_connected()

        # Add prefix if not present
        if not address.startswith(OSC_PREFIX_ANTESCOFO):
            if not address.startswith("/"):
                address = "/" + address
            address = OSC_PREFIX_ANTESCOFO + address.lstrip("/")

        # Convert Python values to OSC values
        osc_args = [to_osc_value(arg) for arg in args]
        self._osc.send(address, *osc_args)

    # Transport control methods

    def load_score(self, filepath: Union[str, Path]):
        """
        Load an Antescofo score file.

        Args:
            filepath: Path to the score file (.asco.txt or similar)
        """
        filepath = str(filepath)
        logger.info(f"Loading score: {filepath}")
        self._send_command(CMD_LOAD, filepath)

    def start(self):
        """Start score playback."""
        logger.info("Starting playback")
        self._send_command(CMD_START)

    def stop(self):
        """Stop score playback."""
        logger.info("Stopping playback")
        self._send_command(CMD_STOP)

    def pause(self):
        """Pause score playback."""
        logger.info("Pausing playback")
        self._send_command(CMD_PAUSE)

    def resume(self):
        """Resume paused playback."""
        logger.info("Resuming playback")
        self._send_command(CMD_RESUME)

    def next_event(self):
        """Skip to the next event in the score."""
        logger.debug("Skipping to next event")
        self._send_command(CMD_NEXTEVENT)

    def prev_event(self):
        """Go back to the previous event in the score."""
        logger.debug("Going to previous event")
        self._send_command(CMD_PREVEVENT)

    def set_tempo(self, tempo: float):
        """
        Set the tempo.

        Args:
            tempo: Tempo in BPM (beats per minute)
        """
        logger.info(f"Setting tempo to {tempo}")
        self._send_command(CMD_TEMPO, float(tempo))

    # OSC configuration methods

    def enable_osc_communication(self, enable: bool = True):
        """
        Enable or disable OSC communication with Ascograph/external systems.

        Args:
            enable: Whether to enable (True) or disable (False)
        """
        self._send_command(CMD_ASCOGRAPHCOMM, 1 if enable else 0)

    def enable_incoming_osc(self, enable: bool = True):
        """
        Enable or disable incoming OSC messages.

        Args:
            enable: Whether to enable (True) or disable (False)
        """
        self._send_command(CMD_INCOMINGOSC, 1 if enable else 0)

    def set_incoming_osc_port(self, port: int):
        """
        Set the port for incoming OSC messages.

        Args:
            port: Port number
        """
        self._send_command(CMD_INCOMING_OSC_PORT, port)

    def configure_ascograph(self, host: str = DEFAULT_HOST, port: int = DEFAULT_ASCOGRAPH_PORT):
        """
        Configure Ascograph communication.

        Args:
            host: Ascograph host
            port: Ascograph port (default: 6789)
        """
        self._send_command(CMD_ASCOGRAPHCONF, host, port)

    # Event subscription methods

    def on(
        self,
        event_type: Optional[Union[EventType, str]],
        handler: Callable[[Event], None],
    ):
        """
        Subscribe to events from Antescofo.

        Args:
            event_type: Type of event to subscribe to (EventType enum or string),
                       or None to subscribe to all events
            handler: Callback function that takes an Event object

        Example:
            >>> def on_tempo_change(event):
            ...     print(f"Tempo changed to: {event.data}")
            >>> client.on(EventType.TEMPO, on_tempo_change)
            >>> # or
            >>> client.on("tempo", on_tempo_change)
        """
        self._ensure_connected()

        # Convert string to EventType if needed
        if isinstance(event_type, str):
            event_type = EventType.from_message(event_type)

        self._osc.subscribe(event_type, handler)

    def off(
        self,
        event_type: Optional[Union[EventType, str]],
        handler: Callable[[Event], None],
    ):
        """
        Unsubscribe from events.

        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler to remove
        """
        self._ensure_connected()

        # Convert string to EventType if needed
        if isinstance(event_type, str):
            event_type = EventType.from_message(event_type)

        self._osc.unsubscribe(event_type, handler)

    # Utility methods

    def wait(self, seconds: float):
        """
        Wait for a specified number of seconds.

        Useful for keeping a script alive while Antescofo is playing.

        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)

    # Context manager support

    def __enter__(self):
        """Context manager entry."""
        if not self._connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def __del__(self):
        """Cleanup on deletion."""
        if self._connected:
            self.disconnect()
