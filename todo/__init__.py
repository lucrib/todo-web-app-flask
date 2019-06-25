from flask import Flask
from flask_restful import Api

from todo.blueprints import register_resources
from todo.client import TodoClient
from todo.exceptions import register_exception_handlers

app = Flask(__name__)
api = Api(app)

__all__ = ['app', 'api', 'TodoClient']

register_exception_handlers(app)
register_resources(api)

if __name__ == '__main__':
    app.run(debug=True)
