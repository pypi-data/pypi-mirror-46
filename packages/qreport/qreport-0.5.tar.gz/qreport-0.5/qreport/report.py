import qreport
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from .db import DB
from enum import Enum
import re
import os

class Report:

    class FieldType(Enum):
        STRING='string'
        TEXT='text'
        DATE='date'
        TIME='time'
        DATETIME='datetime'
        INT='int'
        NUMERIC='numeric'
        DROPDOWN='dropdown'
        MULTISELECT='multiselect'
        HIDDEN='hidden'

    def __init__(self, database_url='sqlite://'):
        self.db = DB(database_url)
        self._title = ''
        self._title = ''
        self._conditions = {}
        self._filters = []
        self._columns = []
        self._display_as = {}
        self._params = {}
        self._callback_columns = {}
        self._field_types = {}
        self._callback_footer = None

    def set_title(self, title):
        self._title = title
        return self

    def set_sql(self, sql):
        self._sql = sql
        return self

    def set_condition(self, condition, value):
        self._conditions[condition] = value
        return self

    def set_filters(self, filters):
        self._filters = [a if type(a) is list else [a] for a in filters]
        return self

    def set_columns(self, columns):
        self._columns = columns
        return self

    def display_as(self, field, label):
        self._display_as[field] = label
        return self

    def set_params(self, params):
        self._params = params
        return self

    def callback_column(self, field, fn):
        self._callback_columns[field] = fn
        return self

    def callback_footer(self, fn):
        """
        Arguments: template, data
        Returns: (template, row)
        Example:
            r = Report('')
            def fn(template, data):
                template = "<tr><th> {nome} </th><th>{telefone}</th></tr>"
                row = {'nome': 'total', 'telefone': '40'}
                return (template, row)

            r.callback_footer(fn)
        """
        self._callback_footer = fn
        return self

    def set_field_type(self, field, field_type=FieldType.STRING, *args, **kwargs):
        """
        - dropdown: use args and/or kwargs to populate a list of options
        - date: uses kwargs format='DD/MM/YYYY', format_out='YYYY-MM-DD'
        - number: uses kwargs format='0,00', format_out='0.00'
        """
        opts = { i:i for i in args}
        opts.update(kwargs)
        ftype = field_type.value if type(field_type) is self.FieldType else field_type
        self._field_types[field] = (ftype, opts)
        return self

    def query(self, sql, *args, **kwargs):
        return self.db.query(sql, *args, **kwargs)

    def get_context(self):
        prefix = 'filter'
        params = {re.sub('^%s[.]' % prefix, '', it[0]): it[1]
                  for it in self._params.items() if it[0].startswith(prefix)}

        data = self.db.get_data(sql=self._sql, columns=self._columns,
            params=params, conditions=self._conditions)

        # Informed or default
        columns = self._columns if self._columns else (data[0] or {}).keys()

        footer = ''
        if self._callback_footer:
            # sorry :(
            template_footer = ''.join(['<th><%{}%></th>'.format(c) for c in columns]).replace('<%','{').replace('%>','}')
            _template, _row = self._callback_footer(template_footer, data)
            d = defaultdict(str)
            d.update(_row)
            _template = _template.replace('{', '{0[').replace('}', ']}')
            footer = _template.format(d)

        return {
            'title': self._title,
            'columns': columns,
            'filters': self._filters,
            'display_as': self._display_as,
            'callback_columns': self._callback_columns,
            'footer': footer,
            'field_types': self._field_types,
            'data': data,
            'params': params,
        }


    def render(self):
        # Validate required
        # templating
        file_loader = FileSystemLoader(qreport.REPORT_TEMPLATE_PATH)
        env = Environment(loader=file_loader)
        template = env.get_template('index.html')

        context = self.get_context()
        return template.render(context)

