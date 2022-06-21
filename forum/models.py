from tkinter import CASCADE
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

