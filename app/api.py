# app/api.py
from flask import Blueprint, request, jsonify

from .models import Todo, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created} for
        todo in todos]
    return jsonify({'todos': todos_list})


@api_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(title=data['title'], description=data.get('description'))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'id': new_todo.id, 'title': new_todo.title, 'description': new_todo.description,
                    'date_created': new_todo.date_created})


@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created})


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data['title']
    todo.description = data.get('description')
    db.session.commit()
    return jsonify(
        {'id': todo.id, 'title': todo.title, 'description': todo.description, 'date_created': todo.date_created})


@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})
