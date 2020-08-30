from .models import Snippet,OnlineIDE
from django import forms
from django_ace import AceWidget


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        widgets = {
            "text": AceWidget(mode='c_cpp', theme='twilight',wordwrap=False, width='100%', height='400px',fontsize="20px", toolbar=True, showprintmargin=True),
        }
        exclude = ()

class EditorForm(forms.Form):
    text = forms.CharField(widget=AceWidget(mode='c_cpp', theme='twilight', wordwrap=False, width="100%", height="400px",fontsize="20px", toolbar=True, showprintmargin=True))

class IDEForm(forms.ModelForm):
    class Meta:
        model = OnlineIDE
        widgets = {
            "text" : AceWidget(mode='c_cpp', theme='twilight',wordwrap=False, width='100%', height='400px',fontsize="20px", toolbar=True, showprintmargin=True)
        }
        exclude = ()
