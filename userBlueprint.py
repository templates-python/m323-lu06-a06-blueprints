from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user
from userDao import UserDao

user_blueprint = Blueprint('user_blueprint', __name__)
user_dao = UserDao('todo_example.db')


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_dao.get_user_by_username(data['username'])
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Invalid username or password'}), 401


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200
