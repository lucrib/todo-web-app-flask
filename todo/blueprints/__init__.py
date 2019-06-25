from todo.blueprints.todo_resource import TodoListResource, TodoResource


def register_resources(api):
    api.add_resource(TodoListResource, '/todos')
    api.add_resource(TodoResource, '/todos/<todo_id>')
