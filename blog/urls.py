from django.urls import path
from .views import (
PostListView,
PostDetailView,
PostCreateView,
PostUpdateView,
PostDeleteView,
)
from users import views as user_view
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about ,name='blog-about'),
    path('topics/',views.topics,name='blog-topic'),
    path('result/<query>',views.search,name='blog-search'),
    path('questions/<query>',views.question_list,name='question-list'),
    path('question/<int:query>',views.question_detail,name='question-detail'),
    path('discussions/<int:query>',views.discussion,name='discussion'),
    path('doubt-like/<int:query>',views.doubt_like,name='doubt-like'),
    path('reply/<int:query>',views.save_reply,name='reply'),
    path('reply/<int:query>/<int:query1>',views.reply_like,name='reply-like'),
    path('contact-admin/',user_view.show_admin,name='contact-admin')
]
