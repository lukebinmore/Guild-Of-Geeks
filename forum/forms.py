from . import models
from django import forms
from django_summernote.widgets import SummernoteWidget
from datetime import datetime
from dateutil.relativedelta import relativedelta


# A class that is used to create a date picker in the form.
class DatePickerInput(forms.DateInput):
    input_type = "date"


# It creates a form for the user to fill out.
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = [
            "content",
        ]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your new comment...",
                    "rows": "4",
                    "maxlength": "1000",
                }
            )
        }
        labels = {"content": ""}


# The class Meta is a nested class that tells Django which model should be
# used to create this form
# (model = Post) and which fields should be used
# (fields = ['title', 'content', 'category', 'tags'])
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title", "content", "category", "tags"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title*"},
            ),
            "category": forms.Select(
                attrs={"class": "form-select select2"},
            ),
            "tags": forms.SelectMultiple(
                attrs={"class": "form-select select2"},
            ),
            "content": SummernoteWidget(
                attrs={
                    "summernote": {"height": "500px"},
                    "placeholder": "Test",
                }
            ),
        }

    def set_category(self, category):
        """
        It takes a dataframe and a category, and returns a dataframe with the
        category added as a column

        :param category: The category of the data
        """
        data = self.data.copy()
        data["category"] = category
        self.data = data

    def set_tags(self, tags):
        """
        It takes a list of tags, and sets the data to the list of tags

        :param tags: a list of strings
        """
        data = self.data.copy()
        data.setlist("tags", tags)
        self.data = data


# It creates a form with two fields, username and password.
class UserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username*"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password*"}
        )
    )


# I'm trying to make a form that allows the user to
# edit their profile information.
class ProfileForm(forms.ModelForm):
    class Meta:
        date_max = datetime.now().date() - relativedelta(years=13)
        model = models.Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "dob",
            "number",
            "picture",
            "theme",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "dob": DatePickerInput(
                attrs={"class": "form-control", "max": date_max}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email Address"}
            ),
            "number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                    "max_length": 12,
                }
            ),
            "picture": forms.FileInput(
                attrs={
                    "class": "form-control profile-picture-upload",
                    "placeholder": "Profile Picture",
                }
            ),
            "theme": forms.Select(
                attrs={"class": "form-select", "placeholder": "Theme"}
            ),
        }


# It creates a form with the fields:
# search, categories, tags, user_posts, followed_posts,
# followed_categories.
class FilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search..."}
        ),
    )
    categories = forms.ModelChoiceField(
        required=False,
        queryset=models.Category.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-select select2 w-100"}
        ),
    )
    tags = forms.ModelChoiceField(
        required=False,
        queryset=models.Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select select2"}),
    )
    user_posts = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mt-0"}),
    )
    followed_posts = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mt-0"}),
    )
    followed_categories = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mt-0"}),
    )


# It creates a form that has 3 fields: old, new, and confirm.
class UpdatePasswordForm(forms.Form):
    old = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current Password*"}
        )
    )
    new = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password*"}
        )
    )
    confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password*"}
        )
    )


# It creates a form that is based on the ContactRequests model.
class ContactForm(forms.ModelForm):
    class Meta:
        model = models.ContactRequests
        fields = [
            "first_name",
            "last_name",
            "email",
            "title",
            "reason",
            "content",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "First Name*",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "Last Name*",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "Email Address*",
                }
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control text-center"}
            ),
            "reason": forms.Select(
                attrs={"class": "form-control text-center"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control text-center"}
            ),
        }


# It creates a form with a password field.
class ConfirmPassword(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password*"}
        )
    )

    def confirm_password(self, user):
        """
        If the user's password matches the password in the form, return True.
        Otherwise, add an error to the password field and return False.

        :param user: The user object that is being edited
        :return: The form is being returned.
        """
        if user.check_password(self.data["password"]):
            return True
        else:
            self.add_error("password", "Invalid password!")
            return False
