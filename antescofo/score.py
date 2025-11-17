"""
Antescofo score file handling.

Provides utilities for reading, writing, and manipulating Antescofo score files.
"""

import logging
from pathlib import Path
from typing import List, Optional, Union

from .exceptions import ScoreError

logger = logging.getLogger(__name__)


class ScoreFile:
    """
    Represents an Antescofo score file.

    Provides methods to read, write, and manipulate score files.
    """

    def __init__(self, content: str = ""):
        """
        Initialize a ScoreFile.

        Args:
            content: Initial content of the score
        """
        self.content = content
        self.lines = content.split("\n") if content else []

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> "ScoreFile":
        """
        Load a score file from disk.

        Args:
            filepath: Path to the score file

        Returns:
            ScoreFile object

        Raises:
            ScoreError: If the file cannot be read
        """
        filepath = Path(filepath)
        try:
            content = filepath.read_text(encoding="utf-8")
            logger.info(f"Loaded score from {filepath}")
            return cls(content)
        except Exception as e:
            raise ScoreError(f"Failed to load score from {filepath}: {e}")

    def save(self, filepath: Union[str, Path]):
        """
        Save the score to a file.

        Args:
            filepath: Path to save the score to

        Raises:
            ScoreError: If the file cannot be written
        """
        filepath = Path(filepath)
        try:
            filepath.write_text(self.content, encoding="utf-8")
            logger.info(f"Saved score to {filepath}")
        except Exception as e:
            raise ScoreError(f"Failed to save score to {filepath}: {e}")

    def append(self, line: str):
        """
        Append a line to the score.

        Args:
            line: Line to append
        """
        self.lines.append(line)
        self.content = "\n".join(self.lines)

    def insert(self, index: int, line: str):
        """
        Insert a line at a specific position.

        Args:
            index: Position to insert at
            line: Line to insert
        """
        self.lines.insert(index, line)
        self.content = "\n".join(self.lines)

    def insert_file(self, filepath: Union[str, Path], quote_if_spaces: bool = True):
        """
        Insert a @insert directive for another file.

        Args:
            filepath: Path to the file to insert
            quote_if_spaces: Whether to quote the filepath if it contains spaces
        """
        filepath_str = str(filepath)
        if quote_if_spaces and " " in filepath_str:
            line = f'@insert "{filepath_str}"'
        else:
            line = f"@insert {filepath_str}"
        self.append(line)

    def insert_file_once(self, filepath: Union[str, Path], quote_if_spaces: bool = True):
        """
        Insert a @insert_once directive for another file.

        Args:
            filepath: Path to the file to insert
            quote_if_spaces: Whether to quote the filepath if it contains spaces
        """
        filepath_str = str(filepath)
        if quote_if_spaces and " " in filepath_str:
            line = f'@insert_once "{filepath_str}"'
        else:
            line = f"@insert_once {filepath_str}"
        self.append(line)

    def add_comment(self, comment: str):
        """
        Add a comment line.

        Args:
            comment: Comment text (will be prefixed with ;)
        """
        self.append(f"; {comment}")

    def add_event(
        self,
        event_type: str,
        duration: Optional[float] = None,
        attributes: Optional[str] = None,
    ):
        """
        Add an event to the score.

        Args:
            event_type: Type of event (e.g., "NOTE", "CHORD")
            duration: Duration of the event
            attributes: Additional attributes
        """
        parts = [event_type]
        if duration is not None:
            parts.append(str(duration))
        if attributes:
            parts.append(attributes)
        self.append(" ".join(parts))

    def add_action(self, action: str):
        """
        Add an action to the score.

        Args:
            action: Action code
        """
        self.append(f"    {action}")

    def add_conditional(self, condition: str, if_block: str, else_block: Optional[str] = None):
        """
        Add a conditional block.

        Args:
            condition: Condition expression
            if_block: Code to execute if condition is true
            else_block: Optional code to execute if condition is false
        """
        self.append(f"#if {condition}")
        for line in if_block.split("\n"):
            self.append(f"  {line}")
        if else_block:
            self.append("#else")
            for line in else_block.split("\n"):
                self.append(f"  {line}")
        self.append("#endif")

    def clear(self):
        """Clear the score content."""
        self.content = ""
        self.lines = []

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        num_lines = len(self.lines)
        return f"ScoreFile({num_lines} lines)"


class ScoreBuilder:
    """
    Builder pattern for constructing Antescofo scores programmatically.

    Example:
        >>> builder = ScoreBuilder()
        >>> builder.comment("My Score")
        >>> builder.event("NOTE", 1.0, "C4 60")
        >>> builder.action("print Hello")
        >>> builder.save("myscore.asco.txt")
    """

    def __init__(self):
        """Initialize the ScoreBuilder."""
        self.score = ScoreFile()

    def comment(self, text: str) -> "ScoreBuilder":
        """
        Add a comment.

        Args:
            text: Comment text

        Returns:
            Self for chaining
        """
        self.score.add_comment(text)
        return self

    def event(
        self,
        event_type: str,
        duration: Optional[float] = None,
        attributes: Optional[str] = None,
    ) -> "ScoreBuilder":
        """
        Add an event.

        Args:
            event_type: Event type
            duration: Duration
            attributes: Attributes

        Returns:
            Self for chaining
        """
        self.score.add_event(event_type, duration, attributes)
        return self

    def action(self, action: str) -> "ScoreBuilder":
        """
        Add an action.

        Args:
            action: Action code

        Returns:
            Self for chaining
        """
        self.score.add_action(action)
        return self

    def insert(self, filepath: Union[str, Path]) -> "ScoreBuilder":
        """
        Insert a file.

        Args:
            filepath: Path to insert

        Returns:
            Self for chaining
        """
        self.score.insert_file(filepath)
        return self

    def insert_once(self, filepath: Union[str, Path]) -> "ScoreBuilder":
        """
        Insert a file once.

        Args:
            filepath: Path to insert

        Returns:
            Self for chaining
        """
        self.score.insert_file_once(filepath)
        return self

    def raw(self, line: str) -> "ScoreBuilder":
        """
        Add a raw line.

        Args:
            line: Line to add

        Returns:
            Self for chaining
        """
        self.score.append(line)
        return self

    def save(self, filepath: Union[str, Path]):
        """
        Save the score to a file.

        Args:
            filepath: Path to save to
        """
        self.score.save(filepath)

    def get_score(self) -> ScoreFile:
        """
        Get the built score.

        Returns:
            The ScoreFile object
        """
        return self.score

    def __str__(self) -> str:
        return str(self.score)
