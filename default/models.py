from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class userEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length=100)
    comments = models.CharField(max_length= 280)
    time = models.IntegerField(default = 0)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class geo(models.Model):
    geojson_object = models.TextField()
    feature = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')
    recent = models.BooleanField(default=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=2)

    def __str__(self):
        return self.geojson_object


class geo30min(models.Model):
    geojson_object = models.TextField()
    feature = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')
    recent = models.BooleanField(default=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(minutes=30)

    def __str__(self):
        return self.geojson_object

class geo2hrs(models.Model):
    geojson_object = models.TextField()
    feature = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')
    recent = models.BooleanField(default=True)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(hours=2)

    def __str__(self):
        return self.geojson_object

class geo6hrs(models.Model):
    geojson_object = models.TextField()
    feature = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')
    recent = models.BooleanField(default=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(hours=6)

    def __str__(self):
        return self.geojson_object


class geoprivate(models.Model):
    geojson_object = models.TextField()
    feature = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')
    recent = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.geojson_object

class eventInfo(models.Model):
    
    popup =  models.ForeignKey(userEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    event_comments = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
 

class privateComments(models.Model):
    comment = models.TextField(null=True)
    pub_date = models.DateTimeField('date published', null=True)
    instance = models.IntegerField()
    author = models.CharField(max_length=280, null=True)
    






