from django.db import models
from datetime import datetime


class FeedUrl(models.Model):
    url = models.URLField()


class FeedDetail(models.Model):
    feed_url = models.ForeignKey(FeedUrl, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, default='asd')
    story_url = models.URLField(default='https://www.google.ca/')
    timestamp = models.TimeField(default=datetime.now().time())
    category = models.CharField(max_length=500, blank=True, null=True)

# class Feeds(models.Model):
#     title = models.CharField(max_length=500)
#     link = models.CharField(max_length=500)
    # category = models.CharField(max_length=500, blank=True)
