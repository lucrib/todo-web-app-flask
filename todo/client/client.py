import requests


class TodoClient(object):
    def __init__(self, client=requests):
        self.client = client

    def get_all_todos(self):
        return self.client.get('/todos')

    def get_todo(self, todo_id):
        return self.client.get(f'/todos/{todo_id}')

    def create_todo(self, data):
        return self.client.post('/todos', json=data)
