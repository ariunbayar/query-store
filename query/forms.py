from django import forms


class ReferenceFilterForm(forms.Form):
    table_name = forms.CharField(max_length=250, required=False)
    column_name = forms.CharField(max_length=250, required=False)