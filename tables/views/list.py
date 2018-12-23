from django.shortcuts import render, redirect, get_object_or_404

from main.utils import execute_query
from tables.models import RemoteTable
from tables.forms import RemoteTableFilterForm


def list(request):
    qs = RemoteTable.objects.all().order_by('owner', 'name')
    num_total = qs.count()

    form = RemoteTableFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('owner'):
            qs = qs.filter(owner__icontains=form.cleaned_data.get('owner'))

    context = {
            'tables': qs,
            'form': form,
            'num_hidden': num_total - qs.count(),
        }

    return render(request, 'tables/list.html', context)
