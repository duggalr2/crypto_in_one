from django.db import models


class Feeds(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    # category = models.CharField(max_length=500, blank=True)
