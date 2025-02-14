import pytest
from datetime import datetime, timedelta

from app.models import Todo


def test_todo_init():
    """Test initialization of To-do object"""
    todo = Todo(1, "Buy milk")
    assert todo.id == 1
    assert todo.text == "Buy milk"
    assert isinstance(todo.timestamp, datetime)
    assert not todo.completed
    assert todo.completion_timestamp is None


def test_todo_switch_completion_initially_incomplete():
    """Test switching completion when initially incomplete"""
    todo = Todo(1, "Buy milk")
    todo.switch_completion()
    assert todo.completed
    assert isinstance(todo.completion_timestamp, datetime)


def test_todo_switch_completion_initially_complete():
    """Test switching completion when initially complete. The completion timestamp remains the COMPLETION timestamp"""
    todo = Todo(1, "Buy milk")
    todo.completed = True
    todo.completion_timestamp = datetime.now()
    first_completion_timestamp = todo.completion_timestamp
    todo.switch_completion()
    assert not todo.completed
    assert todo.completion_timestamp == first_completion_timestamp


def test_todo_switch_completion_multiple_times():
    """Test switching completion multiple times. The completion timestamp only changes upon COMPLETION"""
    todo = Todo(1, "Buy milk")
    todo.switch_completion()
    assert todo.completed
    assert isinstance(todo.completion_timestamp, datetime)
    first_completion_timestamp = todo.completion_timestamp
    todo.switch_completion()
    assert not todo.completed
    assert todo.completion_timestamp == first_completion_timestamp
    todo.switch_completion()
    assert todo.completed
    assert isinstance(todo.completion_timestamp, datetime)
    assert todo.completion_timestamp > first_completion_timestamp


def test_todo_repr():
    """Test representation of To-do object"""
    todo = Todo(1, "Buy milk")
    todo.switch_completion()
    assert repr(
        todo) == f"Todo(text='Buy milk', timestamp={todo.timestamp}, completed=True, completion_timestamp={todo.completion_timestamp})"


def test_todo_timestamp_within_reasonable_range():
    """Test that the timestamp is within a reasonable range"""
    todo = Todo(1, "Buy milk")
    assert (datetime.now() - todo.timestamp) < timedelta(seconds=1)


def test_todo_completion_timestamp_within_reasonable_range():
    """Test that the completion timestamp is within a reasonable range"""
    todo = Todo(1, "Buy milk")
    todo.switch_completion()
    assert (datetime.now() - todo.completion_timestamp) < timedelta(seconds=1)
