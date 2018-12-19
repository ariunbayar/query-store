from django.db import models


class RemoteTable(models.Model):

    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    num_rows = models.IntegerField(default=0)
    is_declared = models.BooleanField(default=False)
    declared_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_name_for_model(self):
        if self.name.startswith('T_'):
            name = self.name[2:]
        else:
            name = self.name

        return 'Ism' + name.replace('_', ' ').title().replace(' ', '')
