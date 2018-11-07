import pickle
import time

from django.shortcuts import render, get_object_or_404
from .models import Query, Ref
from .forms import ReferenceFilterForm
from main.utils import _execute_query


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

    filters = []
    for i in range(1, 5):
        field = request.GET.get('field%s' % i, '')
        value = request.GET.get('value%s' % i, '')
        form['field%s' % i] = field
        form['value%s' % i] = value
        if field and value:
            filters.append((field, value))

    if filters:

        # build column index
        column_index = dict([(col['name'], i) for i, col in enumerate(all_columns)])

        # filter
        rows = []
        for row in all_rows:
            is_matching = all([v in row[column_index[f]] for f, v in filters]) if filters else True
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


def reference(request):
    refs = Ref.objects.all()

    if request.method == 'POST':
        form = ReferenceFilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['table_name']:
                refs = refs.filter(table_name__icontains=form.cleaned_data['table_name'])
            if form.cleaned_data['column_name']:
                refs = refs.filter(column_name__icontains=form.cleaned_data['column_name'])
            if form.cleaned_data['is_listed'] == True:
                refs = refs.filter(is_listed=form.cleaned_data['is_listed'])

    else:
        form = ReferenceFilterForm()

    context = {
            'form': form,
            'refs': refs,
            }
    return render(request, 'query/reference.html', context)
