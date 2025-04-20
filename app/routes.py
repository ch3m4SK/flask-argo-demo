from flask import request, jsonify
from app import db
from app.models import Task
from app.schemas import task_schema, tasks_schema

def register_routes(app):
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify(tasks_schema.dump(tasks))

    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(task_schema.dump(new_task)), 201