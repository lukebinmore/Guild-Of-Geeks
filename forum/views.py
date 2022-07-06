from tkinter import getboolean
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from . import models
from . import forms

class Index(generic.ListView):
    model = models.Post
    queryset = models.Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'forum/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['tags'] = models.Tag.objects.all()
        context['user_form'] = forms.UserForm()
        return context

class PostView(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        paginator = Paginator(post.post_comments.order_by('created_on'), 5)
        page = request.GET.get('page')
        comments = paginator.get_page(page)
        return render(
            request,
            'forum/post.html',
            {
                'post': post,
                'comments': comments,
                'page_obj': comments,
                'new_comment_form': forms.NewCommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        new_comment_form = forms.NewCommentForm(data=request.POST)
        if new_comment_form.is_valid():
            comment = new_comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(request.path)

class PostEdit(View):
    def get(self, request, slug, *args, **kwargs):
        if slug == "new-post":
            post_form = forms.PostForm(
                initial={'title': request.GET['new-post-title'],}
            )

            return render(
                request,
                'forum/post.html',
                {
                    'edit_mode': True,
                    'post_form': post_form,
                }
            )

        else:
            queryset = models.Post.objects.all()
            post = get_object_or_404(queryset, slug=slug)
            paginator = Paginator(post.post_comments.order_by('created_on'), 5)
            page = request.GET.get('page')
            comments = paginator.get_page(page)
            post_form = forms.PostForm(instance=post)

            return render(
                request,
                'forum/post.html',
                {
                    'post': post,
                    'comments': comments,
                    'page_obj': comments,
                    'edit_mode': True,
                    'post_form': post_form,
                },
            )
    
    def post(self, request, slug, *args, **kwargs):
        if slug == 'new-post':
            post_form = forms.PostForm(data=request.POST)
        else:
            queryset = models.Post.objects.all()
            post = get_object_or_404(queryset, slug=slug)
            post_form = forms.PostForm(data=request.POST, instance=post)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            if slug == 'new-post':
                post.slug = slugify(post.title)
                post.author = request.user
                post = post_form.save()
            else:
                post_form.save()

            if 'post-submit-draft' in request.POST:
                post.status = 0
            else:
                post.status = 1

            post.save()

            return redirect('post-view', slug=post.slug)
            
        return redirect('index')

class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        if post.likes.filter(id=self.request.user.id).exists():
            post.likes.remove(request.user)
            return HttpResponse('<i class="far fa-heart"></i> ' + str(post.likes.count()))
        else:
            post.likes.add(request.user)
            return HttpResponse('<i class="fas fa-heart"></i> ' + str(post.likes.count()))

class CommentLike(View):
    def post(self, request, id, *args, **kwargs):
        queryset = models.Comment.objects.all()
        comment = get_object_or_404(queryset, id=id)
        if comment.likes.filter(id=self.request.user.id).exists():
            comment.likes.remove(request.user)
            return HttpResponse('<i class="far fa-heart"></i> ' + str(comment.likes.count()))
        else:
            comment.likes.add(request.user)
            return HttpResponse('<i class="fas fa-heart"></i> ' + str(comment.likes.count()))

class Login(View):
    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(data=request.POST)

        if user_form.is_valid():
            user = authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            return redirect('index')

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/login.html',
            {
                'user_form': forms.UserForm()
            }
        )

class Signup(View):
    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.ProfileForm(data=request.POST)

        if profile_form.is_valid():
            pass
        else:
            return redirect('index')

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/signup.html',
            {
                'profile_form': forms.ProfileForm(),
                'user_form': forms.UserForm()
            }
        )