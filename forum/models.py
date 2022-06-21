from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATE = ((0, "Draft"), (1, "Post"))

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    banner_image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATE, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_categories')
    tags = models.ManyToManyField(Tag, on_delete=models.CASCADE, related_name='blog_tags')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f"{self.content} - (Posted By: {self.author})"