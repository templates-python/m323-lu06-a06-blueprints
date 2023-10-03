import unittest
import json
from main import app, generate_testdata  # Importiere die Flask-App und DAOs aus deinem Modul


class TestTodoAPI(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        generate_testdata()

    def login(self, username, password):
        return self.client.post('/login', json={'username': username, 'password': password})

    def test_login(self):
        response = self.login('admin', 'admin')
        assert response.status_code == 200
        assert json.loads(response.data)['success'] == True

    def test_get_all_todos(self):
        response = self.client.get('/todos')
        assert response.status_code == 200
        assert type(json.loads(response.data)) is list

    def test_add_todo(self):
        self.login('admin', 'admin')
        response = self.client.post('/todos', json={'title': 'Test Todo', 'is_completed': False})
        assert response.status_code == 201
        assert json.loads(response.data)['message'] == 'Todo item created'

    def test_update_todo(self):
        # Logge den Benutzer ein
        self.login('admin', 'admin')

        # Hole alle Todos
        response = self.client.get('/todos')
        assert response.status_code == 200
        todos = json.loads(response.data)

        # Überprüfe, ob die Todo-Liste nicht leer ist
        assert len(todos) > 0

        # Hole die ID des ersten Todo-Elements
        first_todo_id = todos[0]['item_id']

        # Aktualisiere das Todo-Element mit der ersten ID
        response = self.client.put(f'/todos/{first_todo_id}', json={'title': 'Updated Todo', 'is_completed': True})
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Item updated'

    def test_delete_todo(self):
        # Logge den Benutzer ein
        self.login('admin', 'admin')

        # Hole alle Todos
        response = self.client.get('/todos')
        assert response.status_code == 200
        todos = json.loads(response.data)

        # Überprüfe, ob die Todo-Liste nicht leer ist
        assert len(todos) > 0

        # Hole die ID des ersten Todo-Elements
        first_todo_id = todos[0]['item_id']

        # Lösche das Todo-Element mit der ersten ID
        response = self.client.delete(f'/todos/{first_todo_id}')
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Item deleted'
