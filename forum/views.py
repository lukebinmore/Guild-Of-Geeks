from django.shortcuts import render
from django.views import generic, View
from . import models

class PostList(generic.ListView):
    model = models.Post
    template_name = 'base.html'
    queryset = models.Post.objects.filter(status=1).order_by('-created_on')