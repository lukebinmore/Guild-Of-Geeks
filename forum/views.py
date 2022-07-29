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


# This is a view for the index page.
class Index(generic.ListView):
    model = models.Post
    template_name = "forum/index.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        It returns the context data.
        """
        context = super(Index, self).get_context_data(**kwargs)
        context["filters"] = forms.FilterForm(self.request.GET)
        context["user_form"] = forms.UserForm()
        context["post_count"] = self.object_list.count
        return context

    def get_queryset(self):
        """
        It returns a list of objects that match the given lookup parameters.
        """
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        filter_form = forms.FilterForm(data=self.request.GET)
        object_list = models.Post.objects.all()
        query = filter_form.data.get("search", None)
        categories = filter_form.data.getlist("categories")
        tags = filter_form.data.getlist("tags")
        user_posts = filter_form.data.get("user_posts", False)
        followed_posts = filter_form.data.get("followed_posts", False)
        followed_categories = filter_form.data.get(
            "followed_categories", False
        )

        if self.request.user.is_authenticated:
            object_list = object_list.filter(
                Q(status__exact=1) | Q(author__exact=self.request.user)
            )
        else:
            object_list = object_list.filter(status=1)

        if query:
            object_list = object_list.filter(
                Q(title__icontains=query)
                | Q(author__username__icontains=query)
            )

        if categories:
            object_list = object_list.filter(Q(category__id__in=categories))

        if tags:
            object_list = object_list.filter(Q(tags__id__in=tags))

        if user_posts:
            object_list = object_list.filter(
                Q(author__username__exact=self.request.user)
            )

        if followed_posts:
            object_list = object_list.filter(
                Q(id__in=profile.followed_posts.all())
            )

        if followed_categories:
            object_list = object_list.filter(
                Q(
                    category__in=profile.followed_categories.all()
                )
            )
        return object_list


# This is a view for the post view page.
class PostView(View):
    def get(self, request, slug, *args, **kwargs):
        """
        It gets the slug from the url and passes it to the view.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            post = f.get_object(models.Post, slug=slug)
            paginator = Paginator(post.post_comments.order_by("created_on"), 5)
            page = request.GET.get("page")
            comments = paginator.get_page(page)
            return render(
                request,
                "forum/post.html",
                {
                    "post": post,
                    "comments": comments,
                    "page_obj": comments,
                    "new_comment_form": forms.NewCommentForm(),
                },
            )
        except Exception as e:
            messages.error(request, e)

        return redirect(request.path)

    def post(self, request, slug, *args, **kwargs):
        """
        A function that takes in a request, slug, and args and kwargs.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            post = f.get_object(models.Post, slug=slug)
            new_comment_form = forms.NewCommentForm(data=request.POST)
            if new_comment_form.is_valid():
                comment = new_comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                messages.success(request, "Saved new comment!")
                return redirect(request.path)
            else:
                raise Exception(f.form_field_errors(new_comment_form))
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)


# This is a view for the post edit page.
class PostEdit(View):
    def get(self, request, slug, *args, **kwargs):
        """
        It gets the slug from the url and passes it to the view.

        :param request: The request object
        :param slug: the slug of the post
        """
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
        """
        A function that takes in a request, slug, and args and kwargs.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            if slug == "new-post":
                post_form = forms.PostForm(data=request.POST)
            else:
                post = f.get_object(models.Post, slug=slug)
                post_form = forms.PostForm(data=request.POST, instance=post)

            category_title = post_form.data["category"]
            post_form = f.validate_category(post_form, category_title)

            tags = post_form.data.getlist("tags")
            post_form = f.validate_tags(post_form, tags)

            if post_form.has_error("category") or post_form.has_error("tags"):
                return self.return_render(request, slug, post_form)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                if slug == "new-post":
                    post.slug = slugify(post.title)
                    post.author = request.user
                    if models.Post.objects.filter(slug=post.slug).exists():
                        post_form.add_error(
                            "title", "Post with this title already exists!"
                        )
                        return self.return_render(request, slug, post_form)
                    post = post_form.save()
                else:
                    post_form.save()

                if "post-submit-draft" in request.POST:
                    post.status = 0
                else:
                    post.status = 1

                post.save()

                messages.success(request, "Post saved!")

                return redirect("post-view", slug=post.slug)
            else:
                raise Exception(f.form_field_errors(post_form))
        except Exception as e:
            messages.error(request, e)

        return self.return_render(request, slug, post_form)

    def return_render(self, request, slug, form):
        """
        It returns a render.

        :param request: The request object
        :param slug: the slug of the object
        :param form: the form that was submitted
        """
        if slug == "new-post":
            render_dict = {"edit_mode": True, "post_form": form}
        else:
            post = f.get_object(models.Post, slug=slug)
            paginator = Paginator(post.post_comments.order_by("created_on"), 5)
            page = request.GET.get("page")
            comments = paginator.get_page(page)
            render_dict = {
                "post": post,
                "comments": comments,
                "page_obj": comments,
                "edit_mode": True,
                "post_form": form,
            }
        return render(request, "forum/post.html", render_dict)


# This is a view that deletes a post.
class PostDelete(View):
    def get(self, request, slug, *args, **kwargs):
        """
        It gets the slug from the url and passes it to the view.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            return self.return_render(request, slug, forms.ConfirmPassword)
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

    def post(self, request, slug, *args, **kwargs):
        """
        A function that takes in a request, slug, and args and kwargs.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            confirm_form = forms.ConfirmPassword(data=request.POST)
            post = f.get_object(models.Post, slug=slug)
            if confirm_form.is_valid():
                if confirm_form.confirm_password(request.user):
                    post.delete()
                    messages.success(request, "Post deleted!")
                    return f.redirect_page(request, "index")
            else:
                raise Exception(f.form_field_errors(confirm_form))
        except Exception as e:
            messages.error(request, e)
            return f.previous_page(request)

        return self.return_render(request, slug, confirm_form)

    def return_render(self, request, slug, form):
        """
        It returns a render.

        :param request: The request object
        :param slug: the slug of the object
        :param form: the form that was submitted
        """
        return render(
            request,
            "forum/deletepost.html",
            {"post_slug": slug, "confirm_form": form},
        )


# This is a view that likes a post.
class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        """
        A function that takes in a request, a slug, and any number of
        arguments and keyword arguments.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            if not request.user.is_authenticated:
                raise Exception("Please login to Like posts!")
            post = f.get_object(models.Post, slug=slug)
            if post.likes.filter(id=self.request.user.id).exists():
                post.likes.remove(request.user)
                return HttpResponse(
                    '<i class="far fa-heart"></i> ' + str(post.likes.count())
                )
            else:
                post.likes.add(request.user)
                return HttpResponse(
                    '<i class="fas fa-heart text-red"></i> '
                    + str(post.likes.count())
                )
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)


# This is a view that follows a post.
class PostFollow(View):
    def post(self, request, slug, *args, **kwargs):
        """
        A function that takes in a request, slug, and args and kwargs.

        :param request: The request object
        :param slug: the slug of the post
        """
        try:
            if not request.user.is_authenticated:
                raise Exception("Please login to Follow posts!")
            post = f.get_object(models.Post, slug=slug)
            profile = request.user.profile
            if profile.followed_posts.filter(id=post.id).exists():
                profile.followed_posts.remove(post)
                return HttpResponse('<i class="fa-regular fa-star"></i>')
            else:
                profile.followed_posts.add(post)
                return HttpResponse(
                    '<i class="fa-solid fa-star text-red"></i>'
                )
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)


# This is a view that likes a comment.
class CommentLike(View):
    def post(self, request, id, *args, **kwargs):
        """
        A function that takes in a request, id, and args and kwargs.

        :param request: The request object
        :param id: the id of the object you want to update
        """
        try:
            if not request.user.is_authenticated:
                raise Exception("Please login to Like comments!")
            comment = f.get_object(models.Comment, id=id)
            if comment.likes.filter(id=self.request.user.id).exists():
                comment.likes.remove(request.user)
                return HttpResponse(
                    '<i class="far fa-heart"></i> '
                    + str(comment.likes.count())
                )
            else:
                comment.likes.add(request.user)
                return HttpResponse(
                    '<i class="fas fa-heart text-red"></i> '
                    + str(comment.likes.count())
                )
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)


# This is a view that deletes a comment.
class CommentDelete(View):
    def get(self, request, id, *args, **kwargs):
        """
        It gets the id of the object and returns the object.

        :param request: The request object
        :param id: the id of the object
        """
        try:
            return self.return_render(request, id, forms.ConfirmPassword)
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)

    def post(self, request, id, *args, **kwargs):
        """
        A function that takes in a request, id, and args and kwargs.

        :param request: The request object
        :param id: the id of the object you want to update
        """
        try:
            confirm_form = forms.ConfirmPassword(data=request.POST)
            comment = f.get_object(models.Comment, id=id)
            if confirm_form.confirm_password(request.user):
                comment.delete()
                messages.success(request, "Comment deleted!")
                return f.redirect_page(
                    request, "post-view", slug=comment.post.slug
                )
        except Exception as e:
            messages.error(request, e)

        return self.return_render(request, id, confirm_form)

    def return_render(self, request, id, form):
        """
        It returns a render.

        :param request: The request object
        :param id: the id of the object being edited
        :param form: the form that was submitted
        """
        return render(
            request,
            "forum/deletecomment.html",
            {"comment_id": id, "confirm_form": form},
        )


# This is a view that follows a category.
class CategoryFollow(View):
    def post(self, request, id, *args, **kwargs):
        """
        A function that takes in a request, id, and args and kwargs.

        :param request: The request object
        :param id: the id of the object you want to update
        """
        try:
            if not request.user.is_authenticated:
                raise Exception("Please login to Follow categories!")
            category = f.get_object(models.Category, id=id)
            profile = request.user.profile
            if profile.followed_categories.filter(id=category.id).exists():
                profile.followed_categories.remove(category)
                return HttpResponse(category.title)
            else:
                profile.followed_categories.add(category)
                return HttpResponse(
                    '<i class="fa-solid fa-star text-red"></i> '
                    + category.title
                )
        except Exception as e:
            messages.error(request, e)
        return f.previous_page(request)


# This is a view that logs in a user.
class Login(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        return self.return_render(request, forms.UserForm)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            user_form = forms.UserForm(data=request.POST)
            if user_form.is_valid():
                username = user_form.cleaned_data["username"]
                password = user_form.cleaned_data["password"]

                if models.User.objects.filter(username=username).exists():
                    user = authenticate(username=username, password=password)
                    if user is None:
                        user_form.add_error("password", "Password incorrect!")
                    else:
                        login(request, user)
                        messages.success(
                            request, "Welcome back " + user.username
                        )
                        return f.previous_page(request)
                else:
                    user_form.add_error("username", "Username not found!")
            else:
                raise Exception(f.form_field_errors(user_form))
        except Exception as e:
            messages.error(request, e)

        return self.return_render(request, user_form)

    def return_render(self, request, form):
        """
        It returns the render function.

        :param request: The request object
        :param form: the form that was submitted
        """
        return render(request, "forum/login.html", {"user_form": form})


# This is a view that creates a new user account.
class Signup(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        return self.return_render(request, forms.UserForm, forms.ProfileForm)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            user_form = forms.UserForm(data=request.POST)
            profile_form = forms.ProfileForm(
                data=request.POST, files=request.FILES
            )
            if user_form.is_valid() and profile_form.is_valid():
                username = user_form.cleaned_data["username"]
                password = user_form.cleaned_data["password"]
                confirm_password = request.POST.get("confirm")

                user_form = f.validate_username(user_form)
                user_form = f.validate_password(user_form, "password")

                if not user_form.errors:
                    if not models.User.objects.filter(
                        username=username
                    ).exists():
                        if password == confirm_password:
                            user = models.User.objects.create_user(
                                username=username, password=password
                            )

                            profile = profile_form.save(commit=False)
                            profile.user = user
                            profile.save()

                            login(request, user)

                            messages.success(request, f"Welcome {username}!")

                            return f.previous_page(request)
                        else:
                            user_form.add_error(
                                "password", "Passwords do not match!"
                            )
                    else:
                        user_form.add_error(
                            "username", "Username already exists!"
                        )
            else:
                raise Exception(f.form_field_errors(user_form, profile_form))
        except Exception as e:
            messages.error(request, e)

        return self.return_render(request, user_form, profile_form)

    def return_render(self, request, user_form, profile_form):
        """
        It returns the render function.

        :param request: the request object
        :param user_form: &lt;UserCreationForm bound=False, valid=Unknown,
        fields=(username;password1;password2)&gt;
        :param profile_form: &lt;django.forms.models.ModelForm object
        """
        return render(
            request,
            "forum/signup.html",
            {"user_form": user_form, "profile_form": profile_form},
        )


# This is a view that logs a user out.
class Logout(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        logout(request)
        return redirect("index")


# This is a view for the profile page.
class Profile(View):
    def get(self, request, mode, *args, **kwargs):
        """
        A function that gets the request, mode, args, and kwargs.

        :param request: The request object
        :param mode: 'add' or 'edit'
        """
        try:
            if mode == "edit":
                return self.return_render(
                    request, forms.ProfileForm(instance=request.user.profile)
                )
            return render(request, "forum/profile.html")
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            profile_form = forms.ProfileForm(
                data=request.POST,
                files=request.FILES,
                instance=request.user.profile,
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Account updated successfully!")
                return redirect("profile", "view")
            else:
                raise Exception(f.form_field_errors(profile_form))
        except Exception as e:
            messages.error(request, e)

        return redirect(request.path)

    def return_render(self, request, form):
        """
        It returns the render function.

        :param request: The request object
        :param form: the form that was submitted
        """
        return render(
            request,
            "forum/profile.html",
            {"edit_mode": True, "profile_form": form},
        )


# This is a view that updatges a user's password.
class UpdatePassword(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        return self.render_page(request, forms.UpdatePasswordForm)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            password_form = forms.UpdatePasswordForm(data=request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data["old"]
                password_new = password_form.cleaned_data["new"]
                password_confirm = password_form.cleaned_data["confirm"]
                password_form = f.validate_password(password_form, "new")
                print(password_form.errors)
                user = authenticate(
                    username=request.user.username, password=password
                )
                if user:
                    if not password_form.errors:
                        if password_new == password_confirm:
                            user.set_password(password_new)
                            user.save()

                            login(request, user)
                            messages.success(
                                request, "Password updated successfully!"
                            )

                            return f.previous_page(request)
                        else:
                            password_form.add_error(
                                "confirm", "Passwords do not match!"
                            )
                else:
                    password_form.add_error("old", "Incorrect password!")
            else:
                raise Exception(f.form_field_errors(password_form))
        except Exception as e:
            messages.error(request, e)
            return f.previous_page(request)

        return self.render_page(request, password_form)

    def render_page(self, request, form):
        """
        It renders the page.

        :param request: The request object
        :param form: The form that was submitted
        """
        return render(request, "forum/password.html", {"password_form": form})


# This is a view that deletes a user's profile.
class DeleteProfile(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        return self.return_render(request, forms.ConfirmPassword)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            confirm_form = forms.ConfirmPassword(data=request.POST)
            if confirm_form.is_valid():
                if confirm_form.confirm_password(request.user):
                    request.user.profile.delete()
                    request.user.is_active = False
                    request.user.save()
                    messages.success(request, "Profile deleted!")
                    return f.redirect_page(request, "index")
            else:
                raise Exception(f.form_field_errors(confirm_form))
        except Exception as e:
            messages.error(request, e)
            return f.previous_page(request)

        return self.return_render(request, confirm_form)

    def return_render(self, request, form):
        """
        It returns the render function.

        :param request: The request object
        :param form: the form that was submitted
        """
        return render(
            request, "forum/deleteprofile.html", {"confirm_form": form}
        )


# This is a view for the contact us page.
class ContactUs(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        try:
            if request.user.is_authenticated:
                user_dict = {
                    "first_name": request.user.profile.first_name,
                    "last_name": request.user.profile.last_name,
                    "email": request.user.profile.email,
                }
            else:
                user_dict = {}

            return self.return_render(
                request, forms.ContactForm(initial=user_dict)
            )
        except Exception as e:
            messages.error(request, e)
        return redirect(request.path)

    def post(self, request, *args, **kwargs):
        """
        A function that is called when a POST request is made to the server.

        :param request: The request object
        """
        try:
            contact_form = forms.ContactForm(data=request.POST)

            if contact_form.is_valid():
                contact_request = contact_form.save(commit=False)
                if request.user.is_authenticated:
                    contact_request.user = request.user

                contact_request.save()

                messages.success(request, "Request submitted successfully!")

                return redirect("index")
            else:
                raise Exception(f.form_field_errors(contact_form))
        except Exception as e:
            messages.error(request, e)
            return f.previous_page(request)

        return self.return_render(request, contact_form)

    def return_render(self, request, form):
        """
        It returns the render function.

        :param request: The request object
        :param form: the form that was submitted
        """
        return render(request, "forum/contactus.html", {"contact_form": form})


# This is a view for the help page.
class Help(View):
    def get(self, request, *args, **kwargs):
        """
        A function that gets the request, args, and kwargs.

        :param request: The request object
        """
        return render(request, "forum/help.html")
