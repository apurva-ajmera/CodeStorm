from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Question

class Practice(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('practice-create')

class Snippet(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    que_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

class Input(models.Model):
    input_program = models.TextField()

class Input1(models.Model):
    input_program1 = models.TextField()

class OnlineIDE(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
