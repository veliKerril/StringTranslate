from django.db import models


class Requests(models.Model):
    method = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    headers = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
