# Test creating a to-do
from app import db
from app.models import Todo


def test_create_todo_success(client, init_database):
    data = {
        'text': 'Sample to-do'
    }
    response = client.post('/notes/todos', json=data)
    assert response.status_code == 201
    assert b'Todo created successfully!' in response.data

    # Verify the to-do was created
    todo = db.session.get(Todo, 1)  # Use Session.get() instead of Query.get()
    assert todo is not None
    assert todo.text == 'Sample to-do'

def test_create_todo_empty_text(client, init_database):
    data = {}
    response = client.post('notes/todos', json=data)
    assert response.status_code == 201  # Expect success with empty text
    assert b'Todo created successfully!' in response.data

    # Verify that the to-do was created with no text
    todo = db.session.get(Todo, 1)  # Use Session.get() instead of Query.get()
    assert todo is not None
    assert todo.text == ''

# Test retrieving a to-do
def test_get_todo_success(client, init_database):
    todo = Todo(text='Sample to-do')
    db.session.add(todo)
    db.session.commit()

    response = client.get(f'notes/todos/{todo.id}')
    assert response.status_code == 200
    assert response.json['id'] == todo.id
    assert response.json['text'] == todo.text

def test_get_todo_not_found(client, init_database):
    todo_id = 999  # Non-existent to-do
    response = client.get(f'notes/todos/{todo_id}')
    assert response.status_code == 404

# Test updating a to-do
def test_update_todo_success(client, init_database):
    todo = Todo(text='Sample to-do')
    db.session.add(todo)
    db.session.commit()

    data = {
        'text': 'Updated to-do'
    }
    response = client.put(f'notes/todos/{todo.id}', json=data)
    assert response.status_code == 200
    assert b'Todo updated successfully!' in response.data

    # Verify the to-do was updated
    updated_todo = db.session.get(Todo, todo.id)  # Use Session.get() instead of Query.get()
    assert updated_todo.text == 'Updated to-do'

def test_update_todo_not_found(client, init_database):
    todo_id = 999  # Non-existent to-do
    data = {
        'text': 'Updated to-do'
    }
    response = client.put(f'notes/todos/{todo_id}', json=data)
    assert response.status_code == 404

# Test completing a to-do
def test_complete_todo_success(client, init_database):
    todo = Todo(text='Sample to-do')
    db.session.add(todo)
    db.session.commit()

    response = client.put(f'notes/todos/{todo.id}/complete')
    assert response.status_code == 200
    assert b'Todo completed successfully!' in response.data

    # Verify the to-do was completed
    completed_todo = db.session.get(Todo, todo.id)  # Use Session.get() instead of Query.get()
    assert completed_todo.completed is True

def test_complete_todo_not_found(client, init_database):
    todo_id = 999  # Non-existent to-do
    response = client.put(f'notes/todos/{todo_id}/complete')
    assert response.status_code == 404

# Test deleting a to-do
def test_delete_todo_success(client, init_database):
    todo = Todo(text='Sample to-do')
    db.session.add(todo)
    db.session.commit()

    response = client.delete(f'notes/todos/{todo.id}')
    assert response.status_code == 200
    assert b'Todo deleted successfully!' in response.data

    # Verify the to-do was deleted
    deleted_todo = db.session.get(Todo, todo.id)  # Use Session.get() instead of Query.get()
    assert deleted_todo is None

def test_delete_todo_not_found(client, init_database):
    todo_id = 999  # Non-existent to-do
    response = client.delete(f'notes/todos/{todo_id}')
    assert response.status_code == 404