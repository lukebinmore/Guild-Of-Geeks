from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from django.db.models import Q
from . import models
from . import forms

class Index(generic.ListView):
    model = models.Post
    template_name = 'forum/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['filters'] = forms.FilterForm(self.request.GET)
        context['user_form'] = forms.UserForm()
        context['post_count'] = self.object_list.count
        context['search_query'] = self.request.GET.get('q')
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        categories = self.request.GET.get('categories')
        tags = self.request.GET.get('tags')
        user_posts = self.request.GET.get('user_posts')
        followed_posts = self.request.GET.get('followed_posts')
        followed_categories = self.request.GET.get('followed_categories')
        object_list = models.Post.objects.all()

        if self.request.user.is_authenticated:
            object_list = object_list.filter(
                Q(status__exact=1) | Q(author__exact=self.request.user)
            )
        else:
            object_list = object_list.filter(status=1)

        if query != None:
            object_list = object_list.filter(
                Q(title__icontains=query) |
                Q(author__username__icontains=query)
            )
        
        if categories != None:
            object_list = object_list.filter(
                Q(category__id__in=categories)
            )
        
        if tags != None:
            object_list = object_list.filter(
                Q(tags__id__in=tags)
            )

        if user_posts:
            object_list = object_list.filter(
                Q(author__username__exact=self.request.user)
            )

        if followed_posts:
            object_list = object_list.filter(
                Q(id__in=self.request.user.profile.followed_posts.all())
            )
        
        if followed_categories:
            object_list = object_list.filter(
                Q(category__in=self.request.user.profile.followed_categories.all())
            )
        return object_list

class PostView(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.all()
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
        queryset = models.Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        new_comment_form = forms.NewCommentForm(data=request.POST)
        if new_comment_form.is_valid():
            comment = new_comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(request.path)
        else:
            messages.error(request, f'Please fix the following issues:')
            for field in new_comment_form:
                if field.errors is not None:
                    messages.error(request, f' - {field.errors}')
        return redirect(request.path)

class PostEdit(View):
    def get(self, request, slug, *args, **kwargs):
        if slug == "new-post":
            new_post_title = request.GET.get('new-post-title')
            if new_post_title != None:
                post_form = forms.PostForm(initial={'title': new_post_title,})
            else:
                post_form = forms.PostForm(data=request.POST)
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
        try:
            if slug == 'new-post':
                post_form = forms.PostForm(data=request.POST)
            else:
                queryset = models.Post.objects.all()
                post = get_object_or_404(queryset, slug=slug)
                post_form = forms.PostForm(data=request.POST, instance=post)

            category_title = post_form.data['category']
            if not category_title.isdigit():
                if not models.Category.objects.filter(title=category_title).exists():
                    category = models.Category.objects.create(title=category_title)
                    post_form.set_category(category)
            else:
                if not models.Category.objects.filter(id=category_title).exists():
                    raise Exception('Categories may not be just numbers!')
            
            tags = post_form.data.getlist('tags')
            new_tags = []
            for tag in tags:
                if not tag.isdigit():
                    if not models.Tag.objects.filter(title=tag).exists():
                        new_tags.append(models.Tag.objects.create(title=tag))
                else:
                    if not models.Tag.objects.filter(id=tag).exists():
                        raise Exception('Tags may not be just numbers!')
                    else:
                        new_tags.append(tag)
            post_form.set_tags(new_tags)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                if slug == 'new-post':
                    post.slug = slugify(post.title)
                    post.author = request.user
                    if models.Post.objects.filter(slug=post.slug):
                        raise Exception('Post already exists!')
                    post = post_form.save()
                else:
                    post_form.save()

                if 'post-submit-draft' in request.POST:
                    post.status = 0
                else:
                    post.status = 1

                post.save()

                return redirect('post-view', slug=post.slug)
            else:
                for field in post_form:
                    if field.errors:
                        raise Exception(f'{field.name.title()} : {field.errors[0]}')
        except Exception as e:
            messages.error(request, e)

        post_form = forms.PostForm(data=post_form.data)
        if slug == 'new-post':
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

class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        if post.likes.filter(id=self.request.user.id).exists():
            post.likes.remove(request.user)
            return HttpResponse('<i class="far fa-heart"></i> ' + str(post.likes.count()))
        else:
            post.likes.add(request.user)
            return HttpResponse('<i class="fas fa-heart text-red"></i> ' + str(post.likes.count()))

class PostFollow(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = models.Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        profile = request.user.profile
        if profile.followed_posts.filter(id=post.id).exists():
            profile.followed_posts.remove(post)
            return HttpResponse('<i class="fa-regular fa-star"></i>')
        else:
            profile.followed_posts.add(post)
            return HttpResponse('<i class="fa-solid fa-star text-red"></i>')

class CommentLike(View):
    def post(self, request, id, *args, **kwargs):
        queryset = models.Comment.objects.all()
        comment = get_object_or_404(queryset, id=id)
        if comment.likes.filter(id=self.request.user.id).exists():
            comment.likes.remove(request.user)
            return HttpResponse('<i class="far fa-heart"></i> ' + str(comment.likes.count()))
        else:
            comment.likes.add(request.user)
            return HttpResponse('<i class="fas fa-heart text-red"></i> ' + str(comment.likes.count()))

class CommentDelete(View):
    def get(self, request, id, *args, **kwargs):
        print(request.GET.get('post_slug'))
        return render(
            request,
            'forum/deletecomment.html',
            {
                'comment_id': id,
            }
        )
    
    def post(self, request, id, *args, **kwargs):
        confirm = request.POST.get('confirm')
        comment = get_object_or_404(models.Comment.objects.all(), id=id)
        post = get_object_or_404(models.Post.objects.all(), id=comment.post.id)

        try:
            if request.user.check_password(confirm):
                comment.delete()
                return redirect('post-view', post.slug)
            else:
                raise Exception('Incorrect password!')
        except Exception as e:
            messages.error(request, e)

        return redirect('post-view', post.slug)

class CategoryFollow(View):
    def post(self, request, id, *args, **kwargs):
        queryset = models.Category.objects.all()
        category = get_object_or_404(queryset, id=id)
        profile = request.user.profile
        if profile.followed_categories.filter(id=category.id).exists():
            profile.followed_categories.remove(category)
            return HttpResponse(category.title)
        else:
            profile.followed_categories.add(category)
            return HttpResponse('<i class="fa-solid fa-star text-red"></i> ' + category.title)

class Login(View):
    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(data=request.POST)

        try:
            if user_form.is_valid():
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']

                if models.User.objects.filter(username=username).exists():
                    user = authenticate(
                        username = username,
                        password = password
                    )
                    if user is None:
                        raise Exception('Password is incorrect, please try again.')
                    else:
                        login(request, user)
                        messages.success(request, 'Welcome back ' + user.username)
                        return redirect('index')
                else:
                    raise Exception(f'Username {username} not found!')
            else:
                for field in user_form:
                    if field.errors:
                         raise Exception(f'{field.name.title()} : {field.errors[0]}')
        except Exception as e:
            messages.error(request, e)
        
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
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES)

        try:
            if user_form.is_valid() and profile_form.is_valid():
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']
                confirm_password = request.POST.get('confirm')

                if " " in username:
                    raise Exception('Username cannot contain spaces!')

                if not models.User.objects.filter(username=username).exists():
                    if password == confirm_password:
                        user = models.User.objects.create_user(
                            username = username,
                            password = password
                        )

                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()

                        login(request, user)

                        messages.success(request, f'Welcome {username}!')

                        return redirect('index')
                    else:
                        raise Exception(f'Passwords do not match!')
                else:
                    raise Exception(f'Username {username} already exists!')
            else:
                for field in user_form:
                    if field.errors:
                        raise Exception(f'{field.name.title()} : {field.errors[0]}')
                
                for field in profile_form:
                    if field.errors:
                        raise Exception(f'{field.name.title()} : {field.errors[0]}')
        except Exception as e:
            messages.error(request, e)
        
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

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

class Profile(View):
    def get(self, request, mode, *args, **kwargs):
        if mode == 'edit':
            return render(
                request,
                'forum/profile.html',
                {
                    'edit_mode': True,
                    'profile_form': forms.ProfileForm(instance=request.user.profile)
                }
            )
        return render(
            request,
            'forum/profile.html',
        )
    
    def post(self, request, *args,**kwargs):
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        try:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Account updated successfully!')
                return redirect('profile', 'view')
            else:
                for field in profile_form:
                    if field.error:
                        raise Exception(f'{field.name.title()} : {field.error}')
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)

class UpdatePassword(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/password.html',
            {
                'password_form': forms.UpdatePasswordForm()
            }
        )
    
    def post(self, request, *args, **kwargs):
        password_form = forms.UpdatePasswordForm(data=request.POST)

        try:
            if password_form.is_valid():
                password = password_form.cleaned_data['old']
                user = authenticate(
                    username = request.user.username,
                    password = password
                )
                if user is None:
                    raise Exception('Password Incorrect!')
                    
                if password_form.cleaned_data['new'] == password_form.cleaned_data['confirm']:
                    user.set_password(password_form.cleaned_data['new'])
                    user.save()

                    login(request, user)
                    messages.success(request, 'Password updated successfully!')

                    return redirect('index')
                else:
                    raise Exception('Passwords do not match!')
            else:
                for field in password_form:
                    if field.errors:
                        raise Exception(f'{field.name.title()} : {field.errors[0]}')
        except Exception as e:
            messages.error(request, e)
        
        return redirect('index')

class DeleteAccount(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/deleteaccount.html'
        )

    def post(self, request, *args, **kwargs):
        confirm = request.POST.get('confirm')

        try:
            if request.user.check_password(confirm):
                user = get_object_or_404(models.User.objects.all(), username=request.user.username)
                user.delete()
            else:
                raise Exception('Incorrect password!')
        except Exception as e:
            messages.error(request, e)

        return redirect('index')

class ContactUs(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.profile
            user_dict = {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
            }
        else:
            user_dict = {}

        return render(
            request,
            'forum/contactus.html',
            {
                'contact_form': forms.ContactForm(initial=user_dict)
            }
        )
    
    def post(self, request, *args, **kwargs):
        try:
            contact_form = forms.ContactForm(data=request.POST)

            if contact_form.is_valid():
                contact_request = contact_form.save(commit=False)
                if request.user.is_authenticated:
                    contact_request.user = request.user
                contact_request.save()

                messages.success(request, 'Request submitted successfully!')
                
                return render(
                    request,
                    'forum/contactus.html',
                    {
                        'contact_form': forms.ContactForm()
                    }
                )
            else:
                for field in contact_form:
                    if field.errors:
                        raise Exception(f'{field.name.title()} : {field.error}')
        except Exception as e:
            messages.error(request, e)
        
        return render(
            request,
            'forum/contactus.html',
            {
                'contact_form': forms.ContactForm(data=request.POST)
            }
        )

class Help(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/help.html'
        )