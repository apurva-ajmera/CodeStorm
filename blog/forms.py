from django import forms
from .models import Doubt,Reply

class DoubtForm(forms.ModelForm):

    class Meta:
        model = Doubt
        fields = ['ask']

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply']
