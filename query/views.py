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

    all_rows = pickle.loads(query.rows_pickle)
    all_columns = pickle.loads(query.columns_pickle)
    rows = all_rows
    form = {}

    if request.method == 'POST':

        filters = []
        for i in range(1, 5):
            field = request.POST.get('field%s' % i)
            value = request.POST.get('value%s' % i)
            form['field%s' % i] = field
            form['value%s' % i] = value
            if field and value:
                filters.append((field, value))

        # build column index
        column_index = dict([(col['name'], i) for i, col in enumerate(all_columns)])

        # filter
        rows = []
        for row in all_rows:
            is_matching = all([v in row[column_index[f]] for f, v in filters]) if filters else True
            # for i in range(1, 5):
                # field = request.POST.get('field%s' % i)
                # value = request.POST.get('value%s' % i)
                # if field and value:
                    # is_matching = is_matching and value in row[column_index[field]]
            if is_matching:
                rows.append(row)

    context = {
            'form': form,
            'sql': query.query,
            'date': query.updated_at,
            'columns': all_columns,
            'rows': rows,
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
        q.duration_ms = (time.time() - time_started) * 1000
        q.save()

        context['query'] = q


    return render(request, 'query/run_query.html', context)
