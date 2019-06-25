from flask import jsonify


class TodoException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ResourceNotFoundError(TodoException):
    def __init__(self, message):
        super(ResourceNotFoundError, self).__init__(message, 404)


class ValidationError(TodoException):
    def __init__(self, message):
        super(ValidationError, self).__init__(message, 400)


class TodoItemNotFoundError(ResourceNotFoundError):
    def __init__(self, todo_id):
        super(TodoItemNotFoundError, self).__init__(f'Todo {todo_id} not found.')


class InvalidTodoIdError(ValidationError):
    def __init__(self, todo_id):
        super(InvalidTodoIdError, self).__init__(f'{todo_id!r} is not a valid todo id.')


def register_exception_handlers(app):
    @app.errorhandler(TodoException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
