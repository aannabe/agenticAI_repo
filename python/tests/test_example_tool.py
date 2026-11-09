import pytest

from example_tool import summarize


def test_summarize_basic() -> None:
    result = summarize([1, 2, 3])
    assert result["count"] == 3
    assert result["min"] == 1
    assert result["max"] == 3
    assert result["mean"] == pytest.approx(2.0)


def test_summarize_empty_raises() -> None:
    with pytest.raises(ValueError):
        summarize([])
