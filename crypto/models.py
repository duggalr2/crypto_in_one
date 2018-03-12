from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class FeedUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()


class FeedDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed_url = models.ForeignKey(FeedUrl, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, default='asd')
    story_url = models.URLField(default='https://www.google.ca/')
    timestamp = models.TimeField(default=datetime.now().time())
    category = models.CharField(max_length=500, blank=True, null=True)


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()




# class Feeds(models.Model):
#     title = models.CharField(max_length=500)
#     link = models.CharField(max_length=500)
    # category = models.CharField(max_length=500, blank=True)
