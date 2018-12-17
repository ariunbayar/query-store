from django.shortcuts import render, redirect

from main.utils import execute_query
from tables.models import RemoteTable


def _get_remote_tables_sorted():

    query = 'SELECT OWNER, TABLE_NAME, NUM_ROWS FROM ALL_TABLES'

    columns, rows = execute_query(query)

    tables = []
    for owner, name, num_rows in rows:
        tables.append({
                'owner': owner,
                'name': name,
                'is_imported': RemoteTable.objects.filter(owner=owner, name=name).count() > 0,
                'num_rows': num_rows,
            })

    return sorted(tables, key=lambda v: v['owner'] + v['name'])


def remote_tables(request):

    context = {
            'tables': _get_remote_tables_sorted(),
        }

    return render(request, 'tables/remote_tables.html', context)


def remote_tables_import(request):

    tables = _get_remote_tables_sorted()

    for table in tables:
        RemoteTable.objects.get_or_create(
                name=table.get('name'),
                owner=table.get('owner'),
                defaults={
                    'num_rows': table.num_rows,
                    }
            )

    return redirect('table-list')
