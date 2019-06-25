from datetime import datetime
from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource

from todo.exceptions import TodoItemNotFoundError, InvalidTodoIdError
from todo.model.todo_model import Todo, TodoSchema

todo_schema = TodoSchema()

todo1 = Todo(1, 'title', 'description', datetime(2019, 1, 16, 15, 30, 56))
TODO_DB = {1: todo1}


class TodosValidator(object):
    @classmethod
    def validate_new(cls, new_todo):
        pass


class TodoListResource(Resource):
    def get(self):
        """
        Return all the todos
        """
        return jsonify([todo_schema.dump(todo).data for todo in TODO_DB.values()])

    def post(self):
        """
        Receive a new todo and add to the datatabse.
        :return:
        """
        print(request.data)
        new_todo = TodoSchema(exclude=('id',)).load(request.json)
        print(new_todo)
        if new_todo.data is None or new_todo.errors:
            return new_todo.errors, 400
        new_todo = new_todo.data
        TodosValidator.validate_new(new_todo)
        import time
        new_todo.id = time.time_ns()
        TODO_DB[new_todo.id] = new_todo
        return todo_schema.dumps(new_todo).data, HTTPStatus.CREATED.value


class TodoResource(Resource):
    def get(self, todo_id):
        try:
            todo_id = int(todo_id)
        except ValueError:
            raise InvalidTodoIdError(todo_id)
        item = todo_schema.dump(TODO_DB.get(todo_id))
        if item.data:
            return jsonify(item.data)
        else:
            raise TodoItemNotFoundError(todo_id)

    def put(self, todo_id):
        pass

    def delete(self, todo_id):
        pass
