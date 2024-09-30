from flask import Flask, jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from todoItem import TodoItem
from user import User
from todoDao import TodoDao
from userDao import UserDao

app = Flask(__name__)
app.secret_key = 'supersecretkey'

todo_dao = TodoDao('todo_example.db')
user_dao = UserDao('todo_example.db')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user_dao.get_user_by_id(int(user_id))


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_dao.get_user_by_username(data['username'])
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200


@app.route('/todos', methods=['GET'])
def get_all_todos():
    items = todo_dao.get_all_items()
    return jsonify([item.__dict__ for item in items]), 200


@app.route('/todos/<int:item_id>', methods=['GET'])
def get_todo(item_id):
    item = todo_dao.get_item(item_id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({'message': 'Item not found'}), 404


@app.route('/todos', methods=['POST'])
@login_required
def add_todo():
    data = request.get_json()
    new_item = TodoItem(None, data['title'], data['is_completed'])
    todo_dao.add_item(new_item)
    return jsonify({'message': 'Todo item created'}), 201


@app.route('/todos/<int:item_id>', methods=['PUT'])
@login_required
def update_todo(item_id):
    data = request.get_json()
    updated_item = TodoItem(item_id, data['title'], data['is_completed'])
    if todo_dao.update_item(updated_item):
        return jsonify({'message': 'Item updated'}), 200
    else:
        return jsonify({'message': 'Item not found or not updated'}), 404


@app.route('/todos/<int:item_id>', methods=['DELETE'])
@login_required
def delete_todo(item_id):
    if todo_dao.delete_item(item_id):
        return jsonify({'message': 'Item deleted'}), 200
    else:
        return jsonify({'message': 'Item not found or not deleted'}), 404


def generate_testdata():
    # Generate user
    user_dao.create_user_table()
    user_dao.add_user(User(1, 'admin', 'admin@example', 'admin'))

    # Generate todo items
    todo_dao.create_table()
    todo_dao.add_item(TodoItem(1, 'Buy milk', False))
    todo_dao.add_item(TodoItem(2, 'Buy eggs', False))
    todo_dao.add_item(TodoItem(3, 'Buy bread', False))
    todo_dao.add_item(TodoItem(4, 'Buy butter', False))


if __name__ == '__main__':
    generate_testdata()
    app.run(debug=True)
