"""Test aismt."""

import aismt


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(aismt.__name__, str)
