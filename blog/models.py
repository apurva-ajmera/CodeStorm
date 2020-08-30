from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length = 100)
    #content = models.TextField()
    content = RichTextUploadingField(blank=True,null=True,extra_plugins=['codesnippet','youtube',],external_plugin_resources=[('youtube','/static/blog/ckeditor_plugin/youtube/youtube/','plugin.js')])
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Question(models.Model):
    question = models.CharField(max_length = 200)
    Que_definition = RichTextUploadingField(blank=True,null=False,extra_plugins=['codesnippet'])
    tag = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.question

class Doubt(models.Model):
    ask = RichTextUploadingField(blank=True,null=False,extra_plugins=['codesnippet'], config_name='special')
    que_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    like_doubt = models.ManyToManyField(User, related_name='likes_doubt', blank=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

class Reply(models.Model):
    reply = RichTextUploadingField(blank=True,null=False,extra_plugins=['codesnippet'], config_name='reply')
    doubt_id = models.ForeignKey(Doubt, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    like_reply = models.ManyToManyField(User, related_name='likes_reply', blank=True)
#RichTextUploadingField(blank=True,null=False,extra_plugins=['codesnippet'], config_name='special')
