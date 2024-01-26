from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app.models import Todo, db
from . import api_bp
from ..models import User


@api_bp.route('/login', methods=['POST'])
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(message="Already logged in", user=current_user), 200

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(email=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401


@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todos_list = [
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created}
        for todo in todos]
    return jsonify({'todos': todos_list})


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        new_todo = Todo(title=data.get('title'), description=data.get('description'))
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({'id': new_todo.id, 'title': new_todo.title, 'description': new_todo.description,
                        'date_created': new_todo.date_created}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created})


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data['title']
    todo.description = data.get('description')
    db.session.commit()
    return jsonify(
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created})


@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})
