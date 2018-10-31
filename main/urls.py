from django.contrib import admin
from django.urls import path
import query.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', query.views.list, name='query-list'),
    path('run-query/', query.views.run_query, name='query-run'),
    path('query/<int:id>', query.views.detail, name='query-detail'),
]
