from django.shortcuts import render, redirect, HttpResponse
from django.views import generic, View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from django.db.models import Q
from . import models
from . import forms
from . import functions as f

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
        try:
            post = f.get_object(models.Post, slug=slug)
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
        except Exception as e:
            messages.error(request, e)
        
        return redirect(request.path)

    def post(self, request, slug, *args, **kwargs):
        try:
            post = f.get_object(models.Post, slug=slug)
            new_comment_form = forms.NewCommentForm(data=request.POST)
            if new_comment_form.is_valid():
                comment = new_comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                messages.success(request, 'Saved new comment!')
                return redirect(request.path)
            else:
                raise Exception(f.form_field_errors(new_comment_form))
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)

class PostEdit(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            if slug == "new-post":
                post_form = forms.PostForm()
            else:
                post = f.get_object(models.Post, slug=slug)
                post_form = forms.PostForm(instance=post)
            return self.return_render(request, slug, post_form)
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)
    
    def post(self, request, slug, *args, **kwargs):
        try:
            if slug == 'new-post':
                post_form = forms.PostForm(data=request.POST)
            else:
                post = f.get_object(models.Post, slug=slug)
                post_form = forms.PostForm(data=request.POST, instance=post)

            category_title = post_form.data['category']
            post_form = f.validate_category(post_form, category_title)
            
            tags = post_form.data.getlist('tags')
            post_form = f.validate_tags(post_form, tags)

            if post_form.has_error('category') or post_form.has_error('tags'):
                return self.return_render(request, slug, post_form)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                if slug == 'new-post':
                    post.slug = slugify(post.title)
                    post.author = request.user
                    if models.Post.objects.filter(slug=post.slug).exists():
                        post_form.add_error('title', 'Post with this title already exists!')
                        return self.return_render(request, slug, post_form)
                    post = post_form.save()
                else:
                    post_form.save()

                if 'post-submit-draft' in request.POST:
                    post.status = 0
                else:
                    post.status = 1

                post.save()

                messages.success(request, 'Post saved!')

                return redirect('post-view', slug=post.slug)
            else:
                raise Exception(f.form_field_errors(post_form))
        except Exception as e:
            messages.error(request, e)
        
        return self.return_render(request, slug, post_form)
    
    def return_render(self, request, slug, form):
        if slug == 'new-post':
            render_dict = {
                'edit_mode': True,
                'post_form': form
            }
        else:
            post = f.get_object(models.Post, slug=slug)
            paginator = Paginator(post.post_comments.order_by('created_on'), 5)
            page = request.GET.get('page')
            comments = paginator.get_page(page)
            render_dict = {
                'post': post,
                'comments': comments,
                'page_obj': comments,
                'edit_mode': True,
                'post_form': form,
            }
        return render(
            request,
            'forum/post.html',
            render_dict
        )

class PostDelete(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            return self.return_render(request, slug, forms.ConfirmPassword)
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

    def post(self, request, slug, *args, **kwargs):
        try:
            confirm_form = forms.ConfirmPassword(data=request.POST)
            post = f.get_object(models.Post, slug=slug)
            if confirm_form.is_valid():
                if confirm_form.confirm_password(request.user):
                    post.delete()
                    messages.success(request, 'Post deleted!')
                    return f.redirect_page(request, 'index')
            else:
                raise Exception(f.form_field_errors(confirm_form))
        except Exception as e:
            messages.error(request, e)
            return f.previous_page(request)

        return self.return_render(request, slug, confirm_form)
    
    def return_render(self, request, slug, form):
        return render(
            request,
            'forum/deletepost.html',
            {
                'post_slug': slug,
                'confirm_form': form
            }
        )

class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                raise Exception('Please login to Like posts!')
            post = f.get_object(models.Post, slug=slug)
            if post.likes.filter(id=self.request.user.id).exists():
                post.likes.remove(request.user)
                return HttpResponse('<i class="far fa-heart"></i> ' + str(post.likes.count()))
            else:
                post.likes.add(request.user)
                return HttpResponse('<i class="fas fa-heart text-red"></i> ' + str(post.likes.count()))
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

class PostFollow(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                raise Exception('Please login to Follow posts!')
            post = f.get_object(models.Post, slug=slug)
            profile = request.user.profile
            if profile.followed_posts.filter(id=post.id).exists():
                profile.followed_posts.remove(post)
                return HttpResponse('<i class="fa-regular fa-star"></i>')
            else:
                profile.followed_posts.add(post)
                return HttpResponse('<i class="fa-solid fa-star text-red"></i>')
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

class CommentLike(View):
    def post(self, request, id, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                raise Exception('Please login to Like comments!')
            comment = f.get_object(models.Comment, id=id)
            if comment.likes.filter(id=self.request.user.id).exists():
                comment.likes.remove(request.user)
                return HttpResponse('<i class="far fa-heart"></i> ' + str(comment.likes.count()))
            else:
                comment.likes.add(request.user)
                return HttpResponse('<i class="fas fa-heart text-red"></i> ' + str(comment.likes.count()))
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

class CommentDelete(View):
    def get(self, request, id, *args, **kwargs):
        try:
            return self.return_render(request, id, forms.ConfirmPassword)
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)
    
    def post(self, request, id, *args, **kwargs):
        try:
            confirm_form = forms.ConfirmPassword(data=request.POST)
            comment = f.get_object(models.Comment, id=id)
            post = f.get_object(models.Post, id=comment.post.id)
            if confirm_form.confirm_password(request.user):
                comment.delete()
                messages.success(request, 'Comment deleted!')
                return f.redirect_page(request, 'post-view', slug=comment.post.slug)
        except Exception as e:
            messages.error(request, e)

        return self.return_render(request, id, confirm_form)

    def return_render(self, request, id, form):
        return render(
            request,
            'forum/deletecomment.html',
            {
                'comment_id': id,
                'confirm_form': form
            }
        )

class CategoryFollow(View):
    def post(self, request, id, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                raise Exception('Please login to Follow categories!')
            category = f.get_object(models.Category, id=id)
            profile = request.user.profile
            if profile.followed_categories.filter(id=category.id).exists():
                profile.followed_categories.remove(category)
                return HttpResponse(category.title)
            else:
                profile.followed_categories.add(category)
                return HttpResponse('<i class="fa-solid fa-star text-red"></i> ' + category.title)
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

class Login(View):
    def get(self, request, *args, **kwargs):
        return self.return_render(request, forms.UserForm)

    def post(self, request, *args, **kwargs):
        try:
            user_form = forms.UserForm(data=request.POST)
            if user_form.is_valid():
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']

                if models.User.objects.filter(username=username).exists():
                    user = authenticate(
                        username = username,
                        password = password
                    )
                    if user is None:
                        user_form.add_error('password', 'Password incorrect!')
                    else:
                        login(request, user)
                        messages.success(request, 'Welcome back ' + user.username)
                        return f.previous_page(request)
                else:
                    user_form.add_error('username', 'Username not found!')
            else:
                raise Exception(f.form_field_errors(user_form))
        except Exception as e:
            messages.error(request, e)
        
        return self.return_render(request, user_form)
    
    def return_render(self, request, form):
        return render(
            request,
            'forum/login.html',
            {
                'user_form': form
            }
        )

class Signup(View):
    def post(self, request, *args, **kwargs):
        try:
            user_form = forms.UserForm(data=request.POST)
            profile_form = forms.ProfileForm(data=request.POST, files=request.FILES)
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
                raise Exception(f.form_field_errors(user_form, profile_form))
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
        try:
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
        except Exception as e:
            messages.error(request, e)
        return redirect('profile')
    
    def post(self, request, *args,**kwargs):
        try:
            profile_form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Account updated successfully!')
                return redirect('profile', 'view')
            else:
                raise Exception(f.form_field_errors(profile_form))
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
        try:
            password_form = forms.UpdatePasswordForm(data=request.POST)
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
                raise Exception(f.form_field_errors(password_form))
        except Exception as e:
            messages.error(request, e)
        
        return redirect('index')

class DeleteProfile(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'forum/deleteprofile.html'
        )

    def post(self, request, *args, **kwargs):
        try:
            confirm = request.POST.get('confirm')
            if request.user.check_password(confirm):
                user = get_object_or_404(models.User.objects.all(), username=request.user.username)
                user.profile.delete()
                user.is_active = False
                user.save()
                messages.success(request, 'Profile deleted!')
            else:
                raise Exception('Incorrect password!')
        except Exception as e:
            messages.error(request, e)

        return redirect('index')

class ContactUs(View):
    def get(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            messages.error(request, e)
        return redirect('index')
    
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
                raise Exception(f.form_field_errors(contact_form))
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