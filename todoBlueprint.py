from flask import Blueprint
from flask_login import login_required
from flask import jsonify, request
from todoDao import TodoDao
from todoItem import TodoItem

todo_blueprint = Blueprint('todo_blueprint', __name__)
todo_dao = TodoDao('todo_example.db')


@todo_blueprint.route('/todos', methods=['GET'])
def get_all_todos():
    items = todo_dao.get_all_items()
    return jsonify([item.__dict__ for item in items]), 200


@todo_blueprint.route('/todos/<int:item_id>', methods=['GET'])
def get_todo(item_id):
    item = todo_dao.get_item(item_id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({"message": "Item not found"}), 404


@todo_blueprint.route('/todos', methods=['POST'])
@login_required
def add_todo():
    data = request.get_json()
    new_item = TodoItem(None, data['title'], data['is_completed'])
    todo_dao.add_item(new_item)
    return jsonify({"message": "Todo item created"}), 201


@todo_blueprint.route('/todos/<int:item_id>', methods=['PUT'])
@login_required
def update_todo(item_id):
    data = request.get_json()
    updated_item = TodoItem(item_id, data['title'], data['is_completed'])
    if todo_dao.update_item(updated_item):
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"message": "Item not found or not updated"}), 404


@todo_blueprint.route('/todos/<int:item_id>', methods=['DELETE'])
@login_required
def delete_todo(item_id):
    if todo_dao.delete_item(item_id):
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"message": "Item not found or not deleted"}), 404
