"""
Antescofo Python Interface

A Python library for communicating with and controlling Antescofo,
the score following and synchronous programming language for music.

Basic usage:
    >>> from antescofo import AntescofoClient
    >>> client = AntescofoClient()
    >>> client.connect()
    >>> client.load_score("myscore.asco.txt")
    >>> client.start()

For more examples, see the examples/ directory.
"""

import logging

# Core classes
from .client import AntescofoClient
from .events import Event, EventType, ActionTraceEvent, EventDispatcher
from .osc import OSCCommunicator
from .score import ScoreFile, ScoreBuilder
from .types import Tab, Map, AntescofoValue, to_osc_value, from_osc_value

# Configuration utilities
from .util import (
    init_config,
    load_config,
    save_config,
    get_config_value,
    set_config_value,
    resolve_score_path,
    print_config,
)

# Exceptions
from .exceptions import (
    AntescofoException,
    ConnectionError,
    OSCError,
    ScoreError,
    TimeoutError,
    InvalidMessageError,
)

# Constants
from .constants import (
    DEFAULT_ANTESCOFO_PORT,
    DEFAULT_ASCOGRAPH_PORT,
    DEFAULT_HOST,
)

__version__ = "0.1.0"

__all__ = [
    # Main client
    "AntescofoClient",
    # Events
    "Event",
    "EventType",
    "ActionTraceEvent",
    "EventDispatcher",
    # OSC
    "OSCCommunicator",
    # Score
    "ScoreFile",
    "ScoreBuilder",
    # Types
    "Tab",
    "Map",
    "AntescofoValue",
    "to_osc_value",
    "from_osc_value",
    # Configuration
    "init_config",
    "load_config",
    "save_config",
    "get_config_value",
    "set_config_value",
    "resolve_score_path",
    "print_config",
    # Exceptions
    "AntescofoException",
    "ConnectionError",
    "OSCError",
    "ScoreError",
    "TimeoutError",
    "InvalidMessageError",
    # Constants
    "DEFAULT_ANTESCOFO_PORT",
    "DEFAULT_ASCOGRAPH_PORT",
    "DEFAULT_HOST",
]

# Setup logging with a null handler by default
logging.getLogger(__name__).addHandler(logging.NullHandler())
