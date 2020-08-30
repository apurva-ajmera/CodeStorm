import json
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from .forms import DoubtForm,ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.base import RedirectView
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import (
Post,Question,Doubt,Reply
)
from django.template.loader import render_to_string

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 2
    ordering = ['date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

def topics(request):
    return render(request,'blog/topics.html')

def search(request,query):
    context_post={
      'posts' : Post.objects.all(),
      'query' : query
    }
    return render(request,'blog/search.html',context_post)

def question_list(request, query):
    questions = Question.objects.filter(tag=query)

    return render(request, 'blog/question_list.html', {'questions':questions})

def question_detail(request, query):
    questions = Question.objects.filter(id=query)

    return render(request, 'blog/question_detail.html', {'questions':questions})

def save_reply(request, query):
    print(query)
    doubt = Doubt.objects.filter(id=query)
    questions = ""
    id = ""
    for d in doubt:
        question = Question.objects.filter(question=d.que_id)

    for que in question:
        id = que.id
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            for d in doubt:
                form.instance.doubt_id = d
            form.save()

    return redirect('discussion', query=id)

def reply_like(request, query, query1):
    doubt = Doubt.objects.filter(id=query)
    reply = Reply.objects.filter(id=query1)
    for r in reply:
        if r.like_reply.filter(id=request.user.id).exists():
            r.like_reply.remove(request.user)
        else:
            r.like_reply.add(request.user)

    questions = ""
    id = ""
    for d in doubt:
        questions = Question.objects.filter(question=d.que_id)

    for question in questions:
        id = question.id

    return redirect('discussion', query=id)

def doubt_like(request, query):
    doubt = Doubt.objects.filter(id=query)
    #index = request.POST['index']
    for d in doubt:
        if d.like_doubt.filter(id=request.user.id).exists():
            d.like_doubt.remove(request.user)
        else:
            d.like_doubt.add(request.user)

    questions = ""
    id = ""
    doubts = ""
    replys = []
    true = False
    username = request.user
    total_likes=0
    for d in doubt:
        question = Question.objects.filter(question=d.que_id)

    for que in question:
        id = que.id
        #doubts = Doubt.objects.filter(que_id=que)

    #for doubt in doubts:
    #    replys.append(Reply.objects.filter(id=doubt.id))
#
    for d in doubt:
        for user in d.like_doubt.all():
            total_likes += 1
            if user == request.user:
                true = True

    #form = DoubtForm()
    #form1 = ReplyForm()

    #context = {
    #  'form':form,
    #  'form1':form1,
    #  'true':true,
    #  'doubts':doubts,
    #  'username':username,
    #  'replys':replys
    #}

    #return JsonResponse({'dataLike':total_likes,'true':true,'index':index})

    return redirect('discussion',query=id)

def discussion(request, query):
    questions = Question.objects.filter(id=query)
    if request.method == "POST":
        form = DoubtForm(request.POST)
        form1 = ReplyForm()
        if form.is_valid():
            for question in questions:
                form.instance.que_id = question
            form.instance.author = request.user
            form.save()
    else:
        form = DoubtForm()
        form1 = ReplyForm()

    doubts = ""
    replys = []
    true = False
    username = request.user
    for question in questions:
        doubts = Doubt.objects.filter(que_id=question)

    for doubt in doubts:
        for user in doubt.like_doubt.all():
            if user == request.user:
                true = True

    for doubt in doubts:
        replys.append(Reply.objects.filter(doubt_id=doubt.id))

    context = {
      'form':form,
      'form1':form1,
      'true':true,
      'doubts':doubts,
      'username':username,
      'replys':replys
    }

    return render(request, 'blog/discuss.html', context)
