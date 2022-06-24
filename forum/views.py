from django.shortcuts import render
from django.views import generic, View
from . import models

class PostList(generic.ListView):
    model = models.Post
    queryset = models.Post.objects.filter(status=1).order_by('-created_on')

class Index(PostList):
    template_name = 'forum/index.html'