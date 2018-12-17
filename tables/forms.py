from django import forms


class RemoteTableFilterForm(forms.Form):
    owner = forms.CharField(max_length=250, required=False)
    name = forms.CharField(max_length=250, required=False)
