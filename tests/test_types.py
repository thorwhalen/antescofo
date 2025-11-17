"""Tests for Antescofo data types."""

import pytest
from antescofo import Tab, Map, to_osc_value, from_osc_value


class TestTab:
    """Tests for the Tab class."""

    def test_create_empty_tab(self):
        """Test creating an empty tab."""
        tab = Tab()
        assert len(tab) == 0
        assert tab.values == []

    def test_create_tab_with_values(self):
        """Test creating a tab with initial values."""
        tab = Tab([1, 2, 3])
        assert len(tab) == 3
        assert tab.values == [1, 2, 3]

    def test_tab_append(self):
        """Test appending to a tab."""
        tab = Tab()
        tab.append(1)
        tab.append(2)
        assert len(tab) == 2
        assert tab.values == [1, 2]

    def test_tab_indexing(self):
        """Test tab indexing."""
        tab = Tab([10, 20, 30])
        assert tab[0] == 10
        assert tab[1] == 20
        assert tab[2] == 30

    def test_tab_set_item(self):
        """Test setting items in a tab."""
        tab = Tab([1, 2, 3])
        tab[1] = 99
        assert tab[1] == 99

    def test_tab_from_list(self):
        """Test creating tab from list."""
        lst = [1, 2, 3]
        tab = Tab.from_list(lst)
        assert tab.values == [1, 2, 3]
        # Ensure it's a copy
        lst.append(4)
        assert len(tab) == 3

    def test_tab_to_list(self):
        """Test converting tab to list."""
        tab = Tab([1, 2, 3])
        lst = tab.to_list()
        assert lst == [1, 2, 3]
        # Ensure it's a copy
        lst.append(4)
        assert len(tab) == 3

    def test_tab_str(self):
        """Test string representation."""
        tab = Tab([1, 2, 3])
        assert str(tab) == "[1, 2, 3]"


class TestMap:
    """Tests for the Map class."""

    def test_create_empty_map(self):
        """Test creating an empty map."""
        m = Map()
        assert len(m) == 0
        assert m.data == {}

    def test_create_map_with_data(self):
        """Test creating a map with initial data."""
        m = Map({"a": 1, "b": 2})
        assert len(m) == 2
        assert m["a"] == 1
        assert m["b"] == 2

    def test_map_set_item(self):
        """Test setting items in a map."""
        m = Map()
        m["x"] = 10
        m["y"] = 20
        assert m["x"] == 10
        assert m["y"] == 20

    def test_map_get(self):
        """Test get method with default."""
        m = Map({"a": 1})
        assert m.get("a") == 1
        assert m.get("b") is None
        assert m.get("b", 99) == 99

    def test_map_contains(self):
        """Test membership testing."""
        m = Map({"a": 1})
        assert "a" in m
        assert "b" not in m

    def test_map_from_dict(self):
        """Test creating map from dict."""
        d = {"a": 1, "b": 2}
        m = Map.from_dict(d)
        assert m.data == {"a": 1, "b": 2}
        # Ensure it's a copy
        d["c"] = 3
        assert "c" not in m

    def test_map_to_dict(self):
        """Test converting map to dict."""
        m = Map({"a": 1, "b": 2})
        d = m.to_dict()
        assert d == {"a": 1, "b": 2}
        # Ensure it's a copy
        d["c"] = 3
        assert "c" not in m

    def test_map_keys_values_items(self):
        """Test keys, values, items methods."""
        m = Map({"a": 1, "b": 2})
        assert set(m.keys()) == {"a", "b"}
        assert set(m.values()) == {1, 2}
        assert set(m.items()) == {("a", 1), ("b", 2)}


class TestTypeConversion:
    """Tests for type conversion utilities."""

    def test_to_osc_value_primitives(self):
        """Test converting primitive types."""
        assert to_osc_value(42) == 42
        assert to_osc_value(3.14) == 3.14
        assert to_osc_value("hello") == "hello"

    def test_to_osc_value_tab(self):
        """Test converting tabs."""
        tab = Tab([1, 2, 3])
        result = to_osc_value(tab)
        assert result == [1, 2, 3]

    def test_to_osc_value_map(self):
        """Test converting maps."""
        m = Map({"a": 1, "b": 2})
        result = to_osc_value(m)
        # Maps are converted to alternating key-value pairs
        assert "a" in result
        assert 1 in result
        assert "b" in result
        assert 2 in result

    def test_to_osc_value_list(self):
        """Test converting lists."""
        result = to_osc_value([1, 2, 3])
        assert result == [1, 2, 3]

    def test_to_osc_value_nested(self):
        """Test converting nested structures."""
        tab = Tab([1, Tab([2, 3]), 4])
        result = to_osc_value(tab)
        assert result == [1, [2, 3], 4]

    def test_from_osc_value_primitives(self):
        """Test converting OSC primitives back."""
        assert from_osc_value(42) == 42
        assert from_osc_value(3.14) == 3.14
        assert from_osc_value("hello") == "hello"

    def test_from_osc_value_list(self):
        """Test converting OSC lists."""
        result = from_osc_value([1, 2, 3])
        assert isinstance(result, Tab)
        assert result.values == [1, 2, 3]
