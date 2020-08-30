from django.urls import path
from blog.models import Post
from .views import PracticeCreateView
from . import views as practice_views


urlpatterns = [
    path('post/<int:pk>/practice',practice_views.post_practice, name='post-practice'),
    path('practice/new', PracticeCreateView.as_view(), name='practice-create'),
    path('practice/ide/<query>',practice_views.practice_ide, name='practice-online'),
    path('submissions/<int:query>',practice_views.submission, name='submission-list'),
    path('show-submission/<query>',practice_views.show_submission, name='show-submission'),
    path('online-IDE/',practice_views.online_ide, name='ide')
]
