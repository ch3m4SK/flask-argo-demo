from app import ma
from app.models import Task

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)