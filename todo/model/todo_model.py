from marshmallow import Schema, fields, post_load


class Todo(object):
    def __init__(self, id=None, title=None, description=None, due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date

    def __repr__(self):
        return f"""Todo(id={self.id!r}, title={self.title!r}, description={self.description!r}, """ \
            f"""due_date={self.due_date!r})"""


class TodoSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    due_date = fields.DateTime()

    @post_load
    def make(self, data):
        return Todo(**data)
