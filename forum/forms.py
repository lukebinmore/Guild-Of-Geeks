from logging import PlaceHolder
from psycopg2 import Date
from . import models
from django import forms
from django_summernote.widgets import SummernoteWidget

class DatePickerInput(forms.DateInput):
    input_type = 'date'

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
    
    def set_category(self, category):
        data = self.data.copy()
        data['category'] = category
        self.data = data
    
    def set_tags(self, tags):
        data = self.data.copy()
        data.setlist('tags', tags)
        self.data = data

class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Username*'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Password*'
        }
    ))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['first_name', 'last_name', 'email', 'dob', 'number', 'picture', 'dark_mode']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'First Name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Last Name'
                }
            ),
            'dob': DatePickerInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Date Of Birth*'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Email Address'
                }
            ),
            'number': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Phone Number',
                    'max_length': 12
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Profile Picture'
                }
            ),
            'dark_mode': forms.CheckboxInput(
                attrs={
                    'class':'form-check-input',
                    'placeholder':'Dark Mode',
                    'id': 'dark-mode-input'
                }
            ),
        }

class FilterForm(forms.Form):
    categories = forms.ModelChoiceField(
        required=False,
        queryset=models.Category.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select select2 w-100'
        })
    )

    tags = forms.ModelChoiceField(
        required=False,
        queryset=models.Tag.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select select2'
        })
    )
    user_posts = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'filters-user-posts'
        })
    )
    followed_posts = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'filters-followed-posts'
        })
    )
    followed_categories = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'filters-followed-categories'
        })
    )

class UpdatePasswordForm(forms.Form):
    old = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Current Password*'
        }
    ))
    new = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'New Password*'
        }
    ))
    confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password*'
        }
    ))

class ContactForm(forms.Form):
    reason_options = (
        ('Compliment', 'Compliment'),
        ('Complaint', 'Complaint'),
        ('Issue', 'Issue'),
        ('Feature Request', 'Feature Request')
    )
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control text-center',
            'placeholder': 'First Name*'
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control text-center',
            'placeholder': 'Last Name*'
        }
    ))
    reason = forms.MultipleChoiceField(
        choices=reason_options,
        widget=forms.Select(
            attrs={
                'class': 'form-control text-center',
                'placeholder': 'Reason For Contact*'
            })
    )
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control text-center',
            'placeholder': 'Short Title*'
        }
    ))
    content = forms.CharField(widget=SummernoteWidget())