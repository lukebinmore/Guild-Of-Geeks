from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dateutil.relativedelta import relativedelta
from datetime import date

STATE = ((0, 'Draft'), (1, 'Post'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    dob = models.DateField(max_length=8)
    email = models.EmailField(blank=True)
    number = models.CharField(max_length=11, blank=True)
    picture = CloudinaryField('image', default='placeholder')
    dark_mode = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    followed_posts = models.ManyToManyField('Post', related_name='followed_posts', blank=True)
    followed_categories = models.ManyToManyField('Category', related_name='followed_categories', blank=True)

    def __str__(self):
        return self.user.username
    
    def get_age(self):
        return relativedelta(date.today(), self.dob).years


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATE, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_categories')
    tags = models.ManyToManyField(Tag, related_name='blog_tags')
    # comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.post_comments.count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.content} - (Posted By: {self.author})"
