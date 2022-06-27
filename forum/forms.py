from . import models
from django import forms
from django_summernote.widgets import SummernoteWidget

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content',]
        widgets = {
            'content': SummernoteWidget()
        }
        labels = {
            'content': ''
        }