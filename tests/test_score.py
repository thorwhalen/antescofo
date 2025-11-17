"""Tests for Antescofo score handling."""

import tempfile
from pathlib import Path
import pytest
from antescofo import ScoreFile, ScoreBuilder
from antescofo.exceptions import ScoreError


class TestScoreFile:
    """Tests for the ScoreFile class."""

    def test_create_empty_score(self):
        """Test creating an empty score."""
        score = ScoreFile()
        assert score.content == ""
        assert score.lines == []

    def test_create_score_with_content(self):
        """Test creating a score with content."""
        content = "NOTE 1.0 C4 60\n    print hello"
        score = ScoreFile(content)
        assert score.content == content
        assert len(score.lines) == 2

    def test_append_line(self):
        """Test appending lines to a score."""
        score = ScoreFile()
        score.append("NOTE 1.0 C4 60")
        score.append("    print hello")
        assert len(score.lines) == 2
        assert "NOTE" in score.content

    def test_insert_line(self):
        """Test inserting lines at specific positions."""
        score = ScoreFile()
        score.append("Line 1")
        score.append("Line 3")
        score.insert(1, "Line 2")
        assert score.lines == ["Line 1", "Line 2", "Line 3"]

    def test_add_comment(self):
        """Test adding comments."""
        score = ScoreFile()
        score.add_comment("This is a comment")
        assert score.content == "; This is a comment"

    def test_add_event(self):
        """Test adding events."""
        score = ScoreFile()
        score.add_event("NOTE", 1.0, "C4 60")
        assert "NOTE" in score.content
        assert "1.0" in score.content
        assert "C4 60" in score.content

    def test_add_action(self):
        """Test adding actions."""
        score = ScoreFile()
        score.add_action("print hello")
        assert "    print hello" in score.content

    def test_insert_file(self):
        """Test inserting file directives."""
        score = ScoreFile()
        score.insert_file("library.asco.txt")
        assert "@insert library.asco.txt" in score.content

    def test_insert_file_with_spaces(self):
        """Test inserting file with spaces in name."""
        score = ScoreFile()
        score.insert_file("my library.asco.txt")
        assert '@insert "my library.asco.txt"' in score.content

    def test_insert_file_once(self):
        """Test insert_once directive."""
        score = ScoreFile()
        score.insert_file_once("library.asco.txt")
        assert "@insert_once library.asco.txt" in score.content

    def test_add_conditional(self):
        """Test adding conditional blocks."""
        score = ScoreFile()
        score.add_conditional("@arch_darwin", 'print "macOS"', 'print "other"')
        assert "#if @arch_darwin" in score.content
        assert "#else" in score.content
        assert "#endif" in score.content

    def test_clear(self):
        """Test clearing score content."""
        score = ScoreFile("Some content")
        score.clear()
        assert score.content == ""
        assert score.lines == []

    def test_save_and_load(self):
        """Test saving and loading scores."""
        content = "; Test score\nNOTE 1.0 C4 60"
        score = ScoreFile(content)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".asco.txt") as f:
            temp_path = f.name

        try:
            score.save(temp_path)

            # Load it back
            loaded = ScoreFile.load(temp_path)
            assert loaded.content == content
        finally:
            Path(temp_path).unlink()

    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises error."""
        with pytest.raises(ScoreError):
            ScoreFile.load("nonexistent_file.asco.txt")


class TestScoreBuilder:
    """Tests for the ScoreBuilder class."""

    def test_create_builder(self):
        """Test creating a builder."""
        builder = ScoreBuilder()
        assert builder.score is not None

    def test_builder_comment(self):
        """Test adding comments with builder."""
        builder = ScoreBuilder().comment("Test comment")
        assert "; Test comment" in str(builder)

    def test_builder_event(self):
        """Test adding events with builder."""
        builder = ScoreBuilder().event("NOTE", 1.0, "C4 60")
        assert "NOTE" in str(builder)

    def test_builder_action(self):
        """Test adding actions with builder."""
        builder = ScoreBuilder().action("print hello")
        assert "print hello" in str(builder)

    def test_builder_chaining(self):
        """Test method chaining."""
        builder = (
            ScoreBuilder()
            .comment("Header")
            .event("NOTE", 1.0, "C4 60")
            .action("print hello")
            .event("NOTE", 1.0, "D4 62")
        )
        content = str(builder)
        assert "; Header" in content
        assert "NOTE" in content
        assert "print hello" in content

    def test_builder_insert(self):
        """Test inserting files with builder."""
        builder = ScoreBuilder().insert("library.asco.txt")
        assert "@insert library.asco.txt" in str(builder)

    def test_builder_insert_once(self):
        """Test insert_once with builder."""
        builder = ScoreBuilder().insert_once("library.asco.txt")
        assert "@insert_once library.asco.txt" in str(builder)

    def test_builder_raw(self):
        """Test adding raw lines with builder."""
        builder = ScoreBuilder().raw("@global $x := 42")
        assert "@global $x := 42" in str(builder)

    def test_builder_get_score(self):
        """Test getting the built score."""
        builder = ScoreBuilder().comment("Test")
        score = builder.get_score()
        assert isinstance(score, ScoreFile)
        assert "; Test" in score.content

    def test_builder_save(self):
        """Test saving with builder."""
        builder = ScoreBuilder().comment("Test")

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".asco.txt") as f:
            temp_path = f.name

        try:
            builder.save(temp_path)
            loaded = ScoreFile.load(temp_path)
            assert "; Test" in loaded.content
        finally:
            Path(temp_path).unlink()
