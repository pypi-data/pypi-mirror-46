import dataset
from qfilter import qfilter

class DB(object):
    def __init__(self, database_url):
        self.db = dataset.connect(database_url)

    def get_data(self, sql, columns=[], order='', params={}, conditions={}):

        s_from = '({}) t'.format(sql)
        s_select = ','.join(columns) or '*'
        s_order = order

        params.pop('_from', None)
        params.pop('_select', None)

        q = qfilter({
            '_from': s_from,
            '_select': s_select,
            '_order': s_order,
            **params,
            **conditions,
        }, sanitize_from=False)

        # TODO: try/except and loggin error
        rows = self.db.query(q.sql, q.data)
        return [ dict(r) for r in rows]
