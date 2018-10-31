import os
import pickle
import time

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Query


def list(request):
    queries = Query.objects.all().order_by('-created_at')
    context = {
            'queries': queries,
            }

    return render(request, 'query/list.html', context)


def detail(request, id):
    query = get_object_or_404(Query, id=id)

    context = {
            'sql': query.query,
            'date': query.updated_at,
            'columns': pickle.loads(query.columns_pickle),
            'rows': pickle.loads(query.rows_pickle),
            }

    """
    # Table schema
    create_query = (
            "CREATE TABLE `people` (\n"
            "  `id` int(11) NOT NULL AUTO_INCREMENT,\n"
            )

    for col in context['columns']:
        create_query += "  `%s` varchar(250) NULL,\n" % col['name']

    create_query += (
            "  PRIMARY KEY (`id`)\n"
            ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
            )

    import pprint; pprint.pprint(create_query)
    """

    """
    # Data
    insert_query = "INSERT INTO `people` VALUES\n"
    for row in context['rows']:
        values = [str(v).replace("'", "''") for v in row]
        insert_query += "(null,'" + "','".join(values) + "'),\n"
    with open('insert.sql', 'w') as f:
        f.write(insert_query)
    """

    return render(request, 'query/detail.html', context)


def _execute_query(query):

    # https://cx-oracle.readthedocs.io/en/latest/installation.html#quick-start-cx-oracle-installation
    # install cx_Oracle $python -m pip install cx_Oracle --upgrade
    # configure oracle client on PC https://oracle.github.io/odpi/doc/installation.html#linux

    import cx_Oracle

    os.environ["NLS_LANG"] = ".AL32UTF8"

    dsn_tns = cx_Oracle.makedsn(settings.DB_HOST, settings.DB_PORT, settings.DB_SERVER_NAME)
    connection = cx_Oracle.connect(settings.DB_USERNAME, settings.DB_PASSWORD, dsn_tns)

    curs = connection.cursor()

    columns = {}

    def type2str(type):
        if type == cx_Oracle.NUMBER:
            return 'number'
        if type == cx_Oracle.STRING:
            return 'string'
        if type == cx_Oracle.FIXED_CHAR:
            return 'fixed_char'
        if type == cx_Oracle.DATETIME:
            return 'datetime'
        if type == cx_Oracle.LONG_STRING:
            return 'long_string'
        if type == cx_Oracle.BINARY:
            return 'binary'

        return repr(type)


    def get_columns(cursor):
        columns = []
        for field in cursor.description:
            name, type, display_size, internal_size, precision, scale, null_ok = field
            columns.append({
                    'name': name,
                    'type': type2str(type),
                    'display_size': display_size,
                    'internal_size': internal_size,
                    'precision': precision,
                    'scale': scale,
                    'null_ok': null_ok,
                })
        return columns

    curs.execute(query)

    columns = get_columns(curs)

    rows = []
    row = curs.fetchone()
    while row:
        rows.append(row)
        row = curs.fetchone()

    connection.close()

    return columns, rows


def run_query(request):

    context = {}

    if request.method == 'POST':
        query = request.POST.get('query')
        time_started = time.time()
        columns, rows = _execute_query(query)

        q = Query()
        q.query = query
        q.num_columns = len(columns)
        q.num_rows = len(rows)
        q.columns_pickle = pickle.dumps(columns)
        q.rows_pickle = pickle.dumps(rows)
        q.save()

        context['query'] = q


    return render(request, 'query/run_query.html', context)
