"""
Data type mappings between Python and Antescofo.

Antescofo supports several data types:
- Integers (32-bit or 64-bit)
- Floats (32-bit or 64-bit doubles)
- Strings
- Tabs (arrays/lists)
- Maps (dictionaries)
"""

from typing import Any, Dict, List, Union


class Tab:
    """
    Represents an Antescofo tab (array/list).

    Tabs are ordered collections of values that can be of mixed types.
    """

    def __init__(self, values: List[Any] = None):
        """
        Initialize a Tab.

        Args:
            values: List of values to initialize the tab with
        """
        self.values = values if values is not None else []

    def __repr__(self) -> str:
        return f"Tab({self.values})"

    def __str__(self) -> str:
        return f"[{', '.join(str(v) for v in self.values)}]"

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> Any:
        return self.values[index]

    def __setitem__(self, index: int, value: Any):
        self.values[index] = value

    def append(self, value: Any):
        """Add a value to the end of the tab."""
        self.values.append(value)

    def to_list(self) -> List[Any]:
        """Convert to a Python list."""
        return self.values.copy()

    @classmethod
    def from_list(cls, lst: List[Any]) -> "Tab":
        """Create a Tab from a Python list."""
        return cls(lst.copy())


class Map:
    """
    Represents an Antescofo map (associative array/dictionary).

    Maps are collections of key-value pairs.
    """

    def __init__(self, data: Dict[str, Any] = None):
        """
        Initialize a Map.

        Args:
            data: Dictionary to initialize the map with
        """
        self.data = data if data is not None else {}

    def __repr__(self) -> str:
        return f"Map({self.data})"

    def __str__(self) -> str:
        items = ", ".join(f"{k}: {v}" for k, v in self.data.items())
        return f"{{{items}}}"

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key with an optional default."""
        return self.data.get(key, default)

    def keys(self):
        """Return the keys."""
        return self.data.keys()

    def values(self):
        """Return the values."""
        return self.data.values()

    def items(self):
        """Return key-value pairs."""
        return self.data.items()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a Python dictionary."""
        return self.data.copy()

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "Map":
        """Create a Map from a Python dictionary."""
        return cls(dct.copy())


# Type conversion utilities
AntescofoValue = Union[int, float, str, Tab, Map, List, Dict]


def to_osc_value(value: AntescofoValue) -> Any:
    """
    Convert a Python value to an OSC-compatible value.

    Args:
        value: Python value to convert

    Returns:
        OSC-compatible value
    """
    if isinstance(value, Tab):
        return [to_osc_value(v) for v in value.values]
    elif isinstance(value, Map):
        # Maps are more complex; for now, we'll serialize as a list of key-value pairs
        result = []
        for k, v in value.data.items():
            result.extend([k, to_osc_value(v)])
        return result
    elif isinstance(value, (list, tuple)):
        return [to_osc_value(v) for v in value]
    elif isinstance(value, dict):
        result = []
        for k, v in value.items():
            result.extend([str(k), to_osc_value(v)])
        return result
    else:
        return value


def from_osc_value(value: Any) -> AntescofoValue:
    """
    Convert an OSC value to a Python value.

    Args:
        value: OSC value to convert

    Returns:
        Python value
    """
    if isinstance(value, (list, tuple)):
        # Try to detect if this is a map (alternating keys and values)
        if len(value) > 0 and len(value) % 2 == 0:
            # Check if even indices are strings (potential keys)
            if all(isinstance(value[i], str) for i in range(0, len(value), 2)):
                # Could be a map
                data = {}
                for i in range(0, len(value), 2):
                    data[value[i]] = from_osc_value(value[i + 1])
                return Map(data)
        # Otherwise, treat as a tab
        return Tab([from_osc_value(v) for v in value])
    else:
        return value
