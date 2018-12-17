from django.db import models


class RemoteTable(models.Model):

    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    num_rows = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
