import dataset
from qfilter import qfilter

class DB(object):
    def __init__(self, database_url):
        self.db = dataset.connect(database_url)


    def query(self, sql, *args, **kwargs):
        rows = self.db.query(sql, *args, **kwargs)
        return [dict(r) for r in rows]


    def get_data(self, sql, columns=[], order='', params={}, conditions={}):

        s_from = '({}) t'.format(sql)
        s_select = ','.join(columns) or '*'
        s_order = order

        params.pop('_from', None)
        params.pop('_select', None)

        _filters = {
            '_from': s_from,
            '_select': s_select,
            '_order': s_order,
        }
        _filters.update(params)
        _filters.update(conditions)
        q = qfilter(_filters, sanitize_from=False, quote_fields=False)

        # TODO: try/except and loggin error
        rows = self.db.query(q.sql, q.data)
        return [ dict(r) for r in rows]
