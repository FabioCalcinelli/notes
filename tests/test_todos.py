from app import db
from app.models import Todo


def test_create_todo(init_database):
    # Create a new to_do object
    todo = Todo("Buy milk")

    # Save the to_do
    db.session.add(todo)
    db.session.commit()

    # Fetch the to_do and check if it's saved correctly
    saved_todo = Todo.query.first()
    assert saved_todo is not None
    assert saved_todo.text == "Buy milk"
    assert saved_todo.completed is False
    assert saved_todo.completion_timestamp is None


def test_complete_todo(init_database):
    # Create a new to_do object
    todo = Todo("Buy milk")

    # Save the to_do
    db.session.add(todo)
    db.session.commit()

    # Fetch the to_do and complete it
    saved_todo = Todo.query.first()
    saved_todo.complete()
    db.session.commit()

    # Fetch the updated to_do and verify changes
    updated_todo = Todo.query.first()
    assert updated_todo.completed is True
    assert updated_todo.completion_timestamp is not None
    assert updated_todo.completion_timestamp > updated_todo.timestamp


def test_delete_todo(init_database):
    # Create a new to_do object
    todo = Todo("Buy milk")

    # Save the to_do
    db.session.add(todo)
    db.session.commit()

    # Verify the to_do is saved
    assert Todo.query.count() == 1

    # Delete the to_do
    db.session.delete(Todo.query.first())
    db.session.commit()

    # Verify that the to_do is deleted
    assert Todo.query.count() == 0


def test_create_multiple_todos(init_database):
    # Create multiple to_do objects
    todo1 = Todo("Buy milk")
    todo2 = Todo("Walk the dog")
    todo3 = Todo("Do laundry")

    # Save the to_dos
    db.session.add_all([todo1, todo2, todo3])
    db.session.commit()

    # Fetch the to_dos and check if they're saved correctly
    saved_todos = Todo.query.all()
    assert len(saved_todos) == 3
    assert saved_todos[0].text == "Buy milk"
    assert saved_todos[1].text == "Walk the dog"
    assert saved_todos[2].text == "Do laundry"


def test_update_todo(init_database):
    # Create a new to_do object
    todo = Todo("Buy milk")

    # Save the to_do
    db.session.add(todo)
    db.session.commit()

    # Fetch the to_do and update its text
    saved_todo = Todo.query.first()
    saved_todo.text = "Buy eggs"
    db.session.commit()

    # Fetch the updated to_do and verify changes
    updated_todo = Todo.query.first()
    assert updated_todo.text == "Buy eggs"