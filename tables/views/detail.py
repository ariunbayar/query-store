from collections import defaultdict

from django.shortcuts import render, get_object_or_404

from main.utils import execute_query
from tables.models import RemoteTable


def _get_table_columns(owner, table):

    query = (
            'SELECT'
            '    COLUMN_NAME, DATA_TYPE, DATA_LENGTH '
            'FROM ALL_TAB_COLUMNS '
            'WHERE OWNER=:powner AND TABLE_NAME=:ptable'
        )

    columns, rows = execute_query(query, powner=owner, ptable=table)

    table_columns = []
    for col_name, data_type, data_len in rows:
        table_columns.append({
                'name': col_name,
                'data_type': data_type,
                'data_len': data_len,
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


def detail(request, rtable_id):

    rtable = get_object_or_404(RemoteTable, pk=rtable_id)
    columns = _get_detailed_columns(rtable)

    # for cons_name, cons in constraints.items:
        # cons = cons_name,

    context = {
            'table': rtable,
            'columns': columns,
        }



    return render(request, 'tables/detail.html', context)
