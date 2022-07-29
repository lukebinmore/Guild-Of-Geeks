from django.test import TestCase
from . import forms


class TestNewCommentForm(TestCase):
    def setUp(self):
        self.form = forms.NewCommentForm({"content": ""})

    def test_content_is_requied(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("content", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["content"][0], "This field is required."
        )

    def test_fields_are_explcit(self):
        self.assertEqual(self.form.Meta.fields, ["content"])


class TestPostForm(TestCase):
    
    def setUp(self):
        self.form = forms.PostForm(
            {"title": "", "content": "", "category": "", "tags": ""}
        )

    def test_title_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("title", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["title"][0], "This field is required."
        )

    def test_content_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("content", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["content"][0], "This field is required."
        )

    def test_category_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("category", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["category"][0], "This field is required."
        )

    def test_tags_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("tags", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["tags"][0], "This field is required."
        )

    def test_fields_are_explcit(self):
        self.assertEqual(
            self.form.Meta.fields, ["title", "content", "category", "tags"]
        )


class TestUserForm(TestCase):

    def setUp(self):
        self.form = forms.UserForm({"username": "", "password": ""})

    def test_username_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("username", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["username"][0], "This field is required."
        )

    def test_password_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("password", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["password"][0], "This field is required."
        )


class TestProfileForm(TestCase):

    def setUp(self):
        self.form = forms.ProfileForm(
            {
                "first_name": "",
                "last_name": "",
                "email": "",
                "dob": "",
                "number": "",
                "picture": "",
                "theme": "",
            }
        )

    def test_dob_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("dob", self.form.errors.keys())
        self.assertEqual(self.form.errors["dob"][0], "This field is required.")

    def test_fields_are_explicit(self):
        self.assertTrue(
            self.form.Meta.fields,
            [
                "first_name",
                "last_name",
                "email",
                "dob",
                "number",
                "picture",
                "theme",
            ],
        )


class TestUpdatePasswordForm(TestCase):

    def setUp(self):
        self.form = forms.UpdatePasswordForm({"old": "", "new": "", "confirm": ""})

    def test_old_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.fields["old"].required, True)

    def test_new_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.fields["new"].required, True)

    def test_confirm_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.fields["confirm"].required, True)


class TestContactForm(TestCase):

    def setUp(self):
        self.form = forms.ContactForm(
            {
                "first_name": "",
                "last_name": "",
                "email": "",
                "title": "",
                "reason": "",
                "content": "",
            }
        )

    def test_first_name_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("first_name", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["first_name"][0], "This field is required."
        )

    def test_last_name_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("last_name", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["last_name"][0], "This field is required."
        )

    def test_email_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("email", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["email"][0], "This field is required."
        )

    def test_title_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("title", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["title"][0], "This field is required."
        )

    def test_reason_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("reason", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["reason"][0], "This field is required."
        )

    def test_content_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("content", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["content"][0], "This field is required."
        )

    def test_fields_are_explicit(self):
        self.assertTrue(
            self.form.Meta.fields,
            ["first_name", "last_name", "email", "title", "reason", "content"],
        )


class TestConfirmPassword(TestCase):

    def setUp(self):
        self.form = forms.ConfirmPassword({"password": ""})

    def test_password_is_required(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn("password", self.form.errors.keys())
        self.assertEqual(
            self.form.errors["password"][0], "This field is required."
        )
