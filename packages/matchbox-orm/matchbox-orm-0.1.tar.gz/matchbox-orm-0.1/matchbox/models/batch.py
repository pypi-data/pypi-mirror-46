from matchbox.database import db
from matchbox.queries import (
    UpdateQuery,
    InsertQuery,
    DeleteQuery
)


class Batch:

    def __init__(self):
        self.batch = db.conn.batch()
        self.queries = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for g in self.queries:
            if isinstance(g, UpdateQuery):
                kwargs = g.parse_insert()
                ref = g.get_ref(kwargs.pop('id'))
                self.batch.update(ref, kwargs)
            elif isinstance(g, InsertQuery):
                kwargs = g.parse_insert()
                ref = g.get_ref(kwargs.pop('id'))
                self.batch.set(ref, kwargs)
            elif isinstance(g, DeleteQuery):
                # kwargs = g.query.parse_insert()
                ref = g.query.get()
                self.batch.delete(ref)
        self.commit()

    def commit(self):
        self.batch.commit()

    def add(self, query):
        self.queries.append(query)

    def delete(self):
