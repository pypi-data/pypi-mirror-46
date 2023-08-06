# qfilter
Simple report using: jinja2, dataset, qfilter and bootstrap

## usage

```
database_url = "postgres://..."

r = Report(database_url)
r.set_params(request.args.to_dict()) # request using flask
r.set_title('My Simple Report')
r.set_sql('select * table')

return r.render()
```

Other options

Define columns and filters:
```
r.set_filters(['field1__icont', 'field2__any']
r.set_columns(['field1', 'field2'])
```

Set fixed condition used in where clausule:
```
r.set_condition('field3__iends', 'a')
```

Display label of de coluns and filters
```
r.display_as('filed1', 'My Field Label')
r.display_as('filed2__any', 'Searching Field2 with contains')
```

Defining type of search fields
```
options = ['opt1', 'opt2', 'opt3']
r.set_field_type('funcao', Report.FieldType.MULTISELECT, *options)
```

Permit callback of columns
```
r.callback_column('field1', lambda value, row: '<b>{}</b>'.format(value))
```


