"""
Constants for Antescofo communication.
"""

# Default OSC ports
DEFAULT_ANTESCOFO_PORT = 5678
DEFAULT_ASCOGRAPH_PORT = 6789

# Default host
DEFAULT_HOST = "localhost"

# OSC message prefixes
OSC_PREFIX_ANTESCOFO = "/antescofo/"

# Message types sent by Antescofo
MSG_STOP = "stop"
MSG_EVENT_BEATPOS = "event_beatpos"
MSG_RNOW = "rnow"
MSG_TEMPO = "tempo"
MSG_PITCH = "pitch"
MSG_ACTION_TRACE = "action_trace"
MSG_LOAD_SCORE = "loadscore"
MSG_CURRENT_SCORE_APPEND = "current_score_append"

# Action trace types
ACTION_TRACE_TYPES = [
    "message",
    "abort",
    "assignment",
    "osc_recv",
    "conditional",
    "loop",
    "curve",
    "process",
    "function",
]

# Internal commands that can be sent to Antescofo
CMD_ASCOGRAPHCOMM = "ascographcomm"
CMD_INCOMINGOSC = "incomingosc"
CMD_INCOMING_OSC_PORT = "IncmingOscPort"
CMD_ASCOGRAPHCONF = "ascographconf"
CMD_LOAD = "load"
CMD_START = "start"
CMD_STOP = "stop"
CMD_PAUSE = "pause"
CMD_RESUME = "resume"
CMD_TEMPO = "tempo"
CMD_NEXTEVENT = "nextevent"
CMD_PREVEVENT = "prevevent"
