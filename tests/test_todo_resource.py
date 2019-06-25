from datetime import datetime
from http import HTTPStatus

import pytest

from todo import app, TodoClient
from todo.model.todo_model import Todo, TodoSchema


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@pytest.fixture
def todo_client(client):
    """
    Create a new TodoClient instance.
    :param client: The transport client. Defaults to requests library.
    :return:
    :rtype: TodoClient
    """
    yield TodoClient(client)


class TestTodoResource(object):

    def test_get_todo_list(self, todo_client):
        resp = todo_client.get_all_todos()
        assert resp.status_code == HTTPStatus.OK
        d = resp.json
        assert type(d) == list
        assert len(d) == 1
        todo1 = d[0]
        assert 'id' in todo1
        assert todo1['id'] == 1
        assert todo1['title'] == 'title'
        assert todo1['description'] == 'description'
        assert todo1['due_date'] == '2019-01-16T15:30:56+00:00'

    def test_get_todo1(self, todo_client):
        resp = todo_client.get_todo(1)
        assert resp.status_code == HTTPStatus.OK
        todo1 = resp.json
        assert type(todo1) == dict
        assert 'id' in todo1
        assert todo1['id'] == 1
        assert todo1['title'] == 'title'
        assert todo1['description'] == 'description'
        assert todo1['due_date'] == '2019-01-16T15:30:56+00:00'

    def test_get_non_existing_todo(self, todo_client):
        resp = todo_client.get_todo(0)
        assert resp.status_code == HTTPStatus.NOT_FOUND
        error = resp.json
        assert 'message' in error
        assert error['message'] == f'Todo 0 not found.'

    def test_get_todo_item_invalid_id(self, todo_client):
        resp = todo_client.get_todo('invalid')
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        error = resp.json
        assert 'message' in error
        assert error['message'] == f''''invalid' is not a valid todo id.'''

    def test_get_todo_item_space_as_id(self, todo_client):
        resp = todo_client.get_todo(' ')
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        error = resp.json
        assert 'message' in error
        assert error['message'] == f'''' ' is not a valid todo id.'''

    def test_get_todo_item_empty_id(self, todo_client):
        resp = todo_client.get_todo('')
        assert resp.status_code == HTTPStatus.NOT_FOUND
        error = resp.json
        assert error is None


class TestTodoListResource:

    def test_post_todo_item(self, todo_client):
        due_date = datetime.now()
        todo_item = Todo(title='todo', description='todo', due_date=due_date)
        data = TodoSchema(exclude=('id',)).dump(todo_item).data
        resp = todo_client.create_todo(data)
        assert resp.status_code == HTTPStatus.CREATED
        assert 'id' in resp.json
        assert 'title' in resp.json
        assert 'description' in resp.json
        assert 'due_date' in resp.json

    def test_post_todo_item_empty(self, todo_client):
        todo_item = Todo()
        print('\nobject: ', todo_item)
        data = TodoSchema(exclude=('id',)).dump(todo_item).data
        print('data:', data)
        resp = todo_client.create_todo(data)
        print(resp)
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        # assert 'id' in resp.json
        assert 'title' in resp.json
        assert 'description' in resp.json
        assert 'due_date' in resp.json
