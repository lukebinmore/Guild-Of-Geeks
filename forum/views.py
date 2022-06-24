from django.shortcuts import render
from django.views import generic, View
from . import models

class Index(generic.ListView):
    model = models.Post
    queryset = models.Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'forum/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['tags'] = models.Tag.objects.all()
        return context