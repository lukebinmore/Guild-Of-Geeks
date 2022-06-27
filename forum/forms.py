from . import models
from django import forms

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content',)