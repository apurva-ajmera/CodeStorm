from django.shortcuts import render
from django.core.files import File
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SnippetForm,EditorForm,IDEForm
from .models import Snippet,Input,Question,OnlineIDE,Input1,Practice
from django.views.generic import CreateView
import subprocess
import json
import re
import threading

def submission(request, query):
    snippets = Snippet.objects.filter(que_id = query)
    return render(request, 'practice/submission_list.html', {"snippets":snippets})

def show_submission(request, query):
    form = EditorForm()
    snippets = Snippet.objects.filter(id=query)
    questions = ""
    text = ""

    for snippet in snippets:
        questions = Question.objects.filter(question=snippet.que_id)
    for snippet in snippets:
        text = snippet.text

    return render(request, 'practice/showSubmission.html', {'snippets':snippets,'questions':questions,'form':form, 'text':text, 'query':query})

def post_practice(request, **kwargs):
    context = {
        'practices':Practice.objects.all()
    }
    return render(request, 'practice/post_practice.html', context)

class PracticeCreateView(LoginRequiredMixin, CreateView):
    model = Practice
    fields = ['question', 'answer']

    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def practice_ide(request, query):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            input = Input()
            input.input_program = request.POST.get('input_program')
            source = input.input_program
            input_data = bytes(source,"UTF-8")
            f = open('practice/files/program.cpp','w+')
            myFile = File(f)
            doc = str(Snippet.objects.filter(author=request.user).first().text)
            myFile.write(doc)
            myFile.close()
            f.close()
            p1 = subprocess.run('practice/static/TDM-GCC-64/com/g++ practice/files/program.cpp -o practice/files/program.exe',capture_output=True,text=True,shell = False)
            if(p1.stderr):
                result_compiler = str(p1.stderr,"UTF-8")
                return render(request,"practice/practice_online.html",{"form":form,"result":result_compiler})
            else:
                p2 = subprocess.run('practice/files/program.exe',input=input_data,capture_output=True,shell=False)
                return render(request, "practice/practice_online.html", {
                    "form": form,
                    "snippets": Snippet.objects.first(),"result":p2.stdout.decode("UTF-8")
                })

    else:
        form = SnippetForm()

    return render(request, 'practice/practice_online.html',{
    "form": form,
    "snippets": Snippet.objects.first(),
    "user":request.user,
    "query":query
    })

@login_required
def online_ide(request):
    threadLock = threading.Lock()
    if request.method == "POST":
        form = IDEForm(request.POST)
        if form.is_valid():
            threadLock.acquire()
            form.save()
            input = Input1()
            input.input_program1 = request.POST.get('input_program1')
            source = input.input_program1
            input_data = bytes(source,"UTF-8")
            f = open('practice/files/program1.cpp','w+')
            myFile = File(f)
            doc = str(OnlineIDE.objects.filter(author=request.user).first().text)
            myFile.write(doc)
            myFile.close()
            f.close()
            p1 = subprocess.run('practice/static/TDM-GCC-64/com/g++ practice/files/program1.cpp -o practice/files/program1.exe',capture_output=True,text=True,shell = False)
            if(p1.stderr):
                result_compiler = re.split("practice/files/program1.cpp: |practice/files/program1.cpp:\d+:\d+: ",p1.stderr)
                error = ""
                for i in range(len(result_compiler)):
                    if result_compiler[i] != " ":
                        error = error + result_compiler[i]
                threadLock.release()
                return render(request,"practice/online_IDE.html",{"form":form,"result":error})
            else:
                p2 = subprocess.run('practice/files/program1.exe',input=input_data,capture_output=True,shell=False)
                threadLock.release()
                return render(request, "practice/online_IDE.html", {
                    "form": form,
                    "codes": OnlineIDE.objects.first(),"result":p2.stdout.decode("UTF-8")
                })

    else:
        form = IDEForm()
        return render(request, 'practice/online_IDE.html', {
        "form":form,
        "user":request.user,
        })
