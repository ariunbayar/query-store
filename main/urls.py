from django.contrib import admin
from django.urls import path
import query.views
import tables.views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', query.views.list, name='query-list'),
    path('reference/', query.views.reference, name='reference'),
    path('run-query/', query.views.run_query, name='query-run'),
    path('query/<int:id>', query.views.detail, name='query-detail'),

    path('tables/remote/', tables.views.remote_tables, name='remote-tables'),
    path('tables/remote/import/', tables.views.remote_tables_import, name='remote-tables-import'),
    path('tables/remote/update-row-count/', tables.views.update_num_rows, name='remote-tables-update-row-count'),
    path('tables/', tables.views.list, name='table-list'),
    path('tables/<int:rtable_id>', tables.views.detail, name='table-detail'),
    path('tables/<int:rtable_id>/mark-as-declared/', tables.views.mark_as_declared, name='table-mark-as-declared'),

]
