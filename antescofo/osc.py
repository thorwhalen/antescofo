"""
OSC (Open Sound Control) communication layer for Antescofo.

Handles low-level OSC message sending and receiving using python-osc.
"""

import logging
import threading
from typing import Any, Callable, List, Optional, Tuple

from pythonosc import dispatcher as osc_dispatcher
from pythonosc import osc_message_builder, osc_server, udp_client

from .constants import DEFAULT_ANTESCOFO_PORT, DEFAULT_HOST, OSC_PREFIX_ANTESCOFO
from .events import Event, EventType, ActionTraceEvent, EventDispatcher
from .exceptions import OSCError

logger = logging.getLogger(__name__)


class OSCCommunicator:
    """
    Handles OSC communication with Antescofo.

    Manages sending messages to Antescofo and receiving messages from it.
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        send_port: int = DEFAULT_ANTESCOFO_PORT,
        receive_port: Optional[int] = None,
    ):
        """
        Initialize the OSC communicator.

        Args:
            host: Hostname or IP address of the Antescofo instance
            send_port: Port to send messages to Antescofo
            receive_port: Port to receive messages from Antescofo (if None, receiving is disabled)
        """
        self.host = host
        self.send_port = send_port
        self.receive_port = receive_port

        # OSC client for sending
        self._client = udp_client.SimpleUDPClient(host, send_port)

        # OSC server for receiving (if enabled)
        self._server: Optional[osc_server.ThreadingOSCUDPServer] = None
        self._server_thread: Optional[threading.Thread] = None
        self._dispatcher = osc_dispatcher.Dispatcher()

        # Event dispatcher
        self.event_dispatcher = EventDispatcher()

        # Setup message handlers if receiving is enabled
        if receive_port is not None:
            self._setup_handlers()

        logger.info(
            f"OSC Communicator initialized: send to {host}:{send_port}, "
            f"receive on port {receive_port}"
        )

    def _setup_handlers(self):
        """Setup OSC message handlers."""
        # Map all /antescofo/* messages
        self._dispatcher.map(
            f"{OSC_PREFIX_ANTESCOFO}*", self._handle_antescofo_message
        )

        # Catch-all for other messages
        self._dispatcher.set_default_handler(self._handle_unknown_message)

    def _handle_antescofo_message(self, address: str, *args):
        """
        Handle a message from Antescofo.

        Args:
            address: OSC address pattern
            *args: Message arguments
        """
        # Extract the message type from the address
        # e.g., "/antescofo/tempo" -> "tempo"
        message_type = address[len(OSC_PREFIX_ANTESCOFO) :]

        logger.debug(f"Received Antescofo message: {address} {args}")

        # Create appropriate event
        event_type = EventType.from_message(message_type)

        if event_type == EventType.ACTION_TRACE and len(args) >= 6:
            # Parse action trace
            event = ActionTraceEvent(
                action_name=args[0],
                trace_type=args[1],
                father_name=args[2],
                now=float(args[3]),
                rnow=float(args[4]),
                message=args[5] if len(args) > 5 else "",
                raw_address=address,
            )
        else:
            # Generic event
            data = args[0] if len(args) == 1 else args
            event = Event(event_type, data, raw_address=address)

        # Dispatch to event handlers
        self.event_dispatcher.dispatch(event)

    def _handle_unknown_message(self, address: str, *args):
        """Handle messages that don't match known patterns."""
        logger.debug(f"Received unknown message: {address} {args}")
        event = Event(EventType.UNKNOWN, args, raw_address=address)
        self.event_dispatcher.dispatch(event)

    def start_receiving(self):
        """Start the OSC server to receive messages."""
        if self.receive_port is None:
            raise OSCError("Cannot start receiving: no receive_port specified")

        if self._server is not None:
            logger.warning("OSC server already running")
            return

        try:
            self._server = osc_server.ThreadingOSCUDPServer(
                (DEFAULT_HOST, self.receive_port), self._dispatcher
            )
            self._server_thread = threading.Thread(
                target=self._server.serve_forever, daemon=True
            )
            self._server_thread.start()
            logger.info(f"Started OSC server on port {self.receive_port}")
        except Exception as e:
            raise OSCError(f"Failed to start OSC server: {e}")

    def stop_receiving(self):
        """Stop the OSC server."""
        if self._server is not None:
            self._server.shutdown()
            self._server = None
            self._server_thread = None
            logger.info("Stopped OSC server")

    def send(self, address: str, *args):
        """
        Send an OSC message.

        Args:
            address: OSC address pattern (e.g., "/antescofo/tempo")
            *args: Message arguments
        """
        try:
            self._client.send_message(address, args if len(args) > 1 else args[0] if args else None)
            logger.debug(f"Sent OSC message: {address} {args}")
        except Exception as e:
            raise OSCError(f"Failed to send OSC message: {e}")

    def send_raw(self, *args):
        """
        Send raw arguments without an address (for internal Antescofo commands).

        Args:
            *args: Message arguments (first arg typically the command name)
        """
        try:
            # For commands sent directly to the Antescofo object (not via OSC address)
            # we send them as a simple message list
            self._client.send_message("/", list(args))
            logger.debug(f"Sent raw message: {args}")
        except Exception as e:
            raise OSCError(f"Failed to send raw message: {e}")

    def subscribe(
        self, event_type: Optional[EventType], handler: Callable[[Event], None]
    ):
        """
        Subscribe to events.

        Args:
            event_type: Type of event to subscribe to, or None for all events
            handler: Callback function to handle events
        """
        self.event_dispatcher.subscribe(event_type, handler)

    def unsubscribe(
        self, event_type: Optional[EventType], handler: Callable[[Event], None]
    ):
        """
        Unsubscribe from events.

        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler to remove
        """
        self.event_dispatcher.unsubscribe(event_type, handler)

    def close(self):
        """Close the communicator and clean up resources."""
        self.stop_receiving()
        self.event_dispatcher.clear()
        logger.info("OSC Communicator closed")

    def __enter__(self):
        """Context manager entry."""
        if self.receive_port is not None:
            self.start_receiving()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
