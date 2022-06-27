from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from django.core.paginator import Paginator
from . import models

class Index(generic.ListView):
    model = models.Post
    queryset = models.Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'forum/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['tags'] = models.Tag.objects.all()
        return context

class Post(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        paginator = Paginator(post.post_comments.order_by('created_on'), 10)
        page = request.GET.get('page')
        comments = paginator.get_page(page)
        return render(
            request,
            'forum/post.html',
            {
                'post': post,
                'comments': comments,
            },
        )