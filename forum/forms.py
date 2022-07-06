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

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-select select2'},
            ),
            'tags': forms.SelectMultiple(
                attrs={'class': 'form-select select2'},
            ),
            'content': SummernoteWidget()
        }

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

class ProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(
        required=False
    )
    dob = forms.DateField()
    number = forms.CharField(
        required=False
    )
    picture = forms.ImageField(
        required=False
    )
