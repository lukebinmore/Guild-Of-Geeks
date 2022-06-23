from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'dob', 'dark_mode', 'created_on', 'updated_on',)
    list_filter = ('dob', 'dark_mode', 'created_on', 'updated_on', 'followed_posts', 'followed_categories')
    search_fields = ('user', 'first_name', 'last_name', 'dob', 'email', 'number', 'created_on', 'updated_on', 'followed_posts', 'followed_categories',)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on',)
    list_filter = ('created_on',)
    search_fields = ('title',)

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('title',)

@admin.register(models.Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on', 'status', 'category', 'likes_count',)
    list_filter = ('author', 'created_on', 'updated_on', 'status', 'category', 'tags',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author', 'created_on', 'updated_on', 'status', 'category', 'tags',)
    summernote_fields = ('content')

@admin.register(models.Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('author', 'post', 'created_on', 'reply_to',)
    list_filter = ('author', 'post', 'created_on', 'reply_to',)
    search_fields = ('author', 'post', 'created_on', 'reply_to',)
    summernote_fields = ('content')