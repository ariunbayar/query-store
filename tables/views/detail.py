from collections import defaultdict

from django.shortcuts import render, get_object_or_404, redirect

from main.utils import execute_query
from tables.models import RemoteTable


def _get_table_columns(owner, table):

    query = (
            'SELECT'
            '    COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE '
            'FROM ALL_TAB_COLUMNS '
            'WHERE OWNER=:powner AND TABLE_NAME=:ptable'
        )

    columns, rows = execute_query(query, powner=owner, ptable=table)

    table_columns = []
    for col_name, data_type, data_len, nullable in rows:
        table_columns.append({
                'name': col_name,
                'data_type': data_type,
                'data_len': data_len,
                'nullable': nullable == 'Y',
            })

    return sorted(table_columns, key=lambda v: v['name'])


def _get_constraints(owner, table):

    query = (
            'SELECT'
            '    CONSTRAINT_NAME, COLUMN_NAME, POSITION '
            'FROM ALL_CONS_COLUMNS '
            'WHERE OWNER=:powner AND TABLE_NAME=:ptable'
        )
    rows = execute_query(query, powner=owner, ptable=table)[1]

    # Ref. about the constraint types: https://docs.oracle.com/database/121/REFRN/GUID-9C96DA92-CFE0-4A3F-9061-C5ED17B43EFE.htm
    query = (
            'SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, SEARCH_CONDITION '
            'FROM ALL_CONSTRAINTS '
            'WHERE OWNER=:powner AND TABLE_NAME=:ptable'
        )
    cons_types = dict([(cname, (ctype, cond))for cname, ctype, cond in execute_query(query, powner=owner, ptable=table)[1]])

    constraints = defaultdict(list)
    rows = sorted(rows, key=lambda v: '%s-%s-%s' % (v[1], v[2], v[0]))
    for constraint_name, column_name, position in rows:
        constraints[column_name].append({
                'name': constraint_name,
                'type': cons_types[constraint_name][0],
                'condition': cons_types[constraint_name][1],
            })

    return constraints


def _get_detailed_columns(rtable):

    constraints = _get_constraints(rtable.owner, rtable.name)
    columns = _get_table_columns(rtable.owner, rtable.name)

    for column in columns:
        column['constraints'] = constraints[column['name']]

    return sorted(columns, key=lambda v: '-'.join([c['name'] for c in v['constraints']]) if v['constraints'] else '{')


def _get_model_declaration(rtable, columns):

    def _get_field_declaration(data_type, data_length, nullable):

        props = []

        if nullable:
            props.append('null=True')

        if data_type in ['NUMBER', 'LONG']:
            field_type = 'IntegerField'
        elif data_type in ['CHAR', 'VARCHAR2']:
            props.append('max_length=%s' % data_length)
            field_type = 'CharField'
        elif data_type in ['DATE']:
            field_type = 'DateTimeField'
        elif data_type in ['FLOAT']:
            field_type = 'FloatField'
        else:
            field_type = '???'

        return "models.%s(%s)" % (field_type, ', '.join(props))


    declaration = "class %s(models.Model):" % rtable.get_name_for_model()
    declaration += "\n\n    class Meta:\n"
    declaration += "        db_table = 'ISM_%s'\n\n" % rtable.name
    declaration += "    change_id = models.IntegerField()\n"
    declaration += "    row_id = models.CharField(max_length=50)\n"

    for col in columns:
        field_name = "f_" + col['name'].lower()
        field_declaration = _get_field_declaration(
                col['data_type'],
                col['data_len'],
                col['nullable'],
            )
        declaration += "\n    " + field_name + " = " + field_declaration

    return declaration


def detail(request, rtable_id):

    rtable = get_object_or_404(RemoteTable, pk=rtable_id)
    columns = _get_detailed_columns(rtable)

    model_declaration = _get_model_declaration(rtable, columns)

    context = {
            'table': rtable,
            'columns': columns,
            'model_declaration': model_declaration,
        }

    return render(request, 'tables/detail.html', context)


def mark_as_declared(request, rtable_id):
    rtable = get_object_or_404(RemoteTable, pk=rtable_id)

    rtable.is_declared = True
    rtable.declared_name = rtable.get_name_for_model()
    rtable.save()

    return redirect('table-detail', rtable_id)
