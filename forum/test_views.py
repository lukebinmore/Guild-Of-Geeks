from django.test import TestCase, RequestFactory
from django.urls import reverse
from . import views, models


class TestIndexView(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.factory = RequestFactory()
        self.data = {"search": "Test"}

    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("forum/index.html")

    def test_index_get_user(self):
        request = self.factory.get(reverse("index"))
        request.user = self.user
        response = views.Index.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("forum/index.html")

    def test_index_get_with_data(self):
        request = self.factory.get(reverse("index"), self.data)
        request.user = self.user
        response = views.Index.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestPostView(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.category = models.Category.objects.create(title="test category")
        self.tag = models.Tag.objects.create(title="Example tag")
        self.post = models.Post.objects.create(
            title="Testing",
            slug="testing",
            author=self.user,
            content="this is a test",
            status=1,
            category=self.category,
        )
        self.post.save()
        self.post.tags.add(self.tag)
        self.factory = RequestFactory()

    def test_post_view_get(self):
        request = self.factory.get(
            reverse("post-view", kwargs={"slug": self.post.slug})
        )
        request.user = self.user
        response = views.PostView.as_view()(request, slug=self.post.slug)
        self.assertEquals(response.status_code, 200)


class TestPostEdit(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.category = models.Category.objects.create(title="test category")
        self.tag = models.Tag.objects.create(title="Example tag")
        self.post = models.Post.objects.create(
            title="Testing",
            slug="testing",
            author=self.user,
            content="this is a test",
            status=1,
            category=self.category,
        )
        self.post.save()
        self.post.tags.add(self.tag)
        self.factory = RequestFactory()

    def test_post_edit_get(self):
        request = self.factory.get(
            reverse("post-edit", kwargs={"slug": self.post.slug})
        )
        request.user = self.user
        response = views.PostView.as_view()(request, slug=self.post.slug)
        self.assertEquals(response.status_code, 200)


class TestPostdelete(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.category = models.Category.objects.create(title="test category")
        self.tag = models.Tag.objects.create(title="Example tag")
        self.post = models.Post.objects.create(
            title="Testing",
            slug="testing",
            author=self.user,
            content="this is a test",
            status=1,
            category=self.category,
        )
        self.post.save()
        self.post.tags.add(self.tag)
        self.factory = RequestFactory()

    def test_post_delete_get(self):
        request = self.factory.get(
            reverse("post-delete", kwargs={"slug": self.post.slug})
        )
        request.user = self.user
        response = views.PostView.as_view()(request, slug=self.post.slug)
        self.assertEquals(response.status_code, 200)


class TestLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_login_get(self):
        request = self.factory.get(reverse("login"))
        response = views.Login.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestSignup(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_get(self):
        request = self.factory.get(reverse("signup"))
        response = views.Login.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestLogout(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_logout_get(self):
        request = self.factory.get(reverse("logout"))
        response = views.Login.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestProfile(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.factory = RequestFactory()

    def test_profile_view_get(self):
        request = self.factory.get(reverse("profile", kwargs={"mode": "view"}))
        request.user = self.user
        response = views.Profile.as_view()(request, mode="view")
        self.assertEquals(response.status_code, 200)

    def test_profile_edit_get(self):
        request = self.factory.get(reverse("profile", kwargs={"mode": "edit"}))
        request.user = self.user
        response = views.Profile.as_view()(request, mode="edit")
        self.assertEquals(response.status_code, 200)


class TestUpdatePassword(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.factory = RequestFactory()

    def test_password_view_get(self):
        request = self.factory.get(reverse("password"))
        request.user = self.user
        response = views.UpdatePassword.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestDeleteProfile(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username="testuser123", password="abcd1234@!"
        )
        self.profile = models.Profile.objects.create(
            user=self.user, dob="1996-07-03"
        )
        self.factory = RequestFactory()

    def test_delete_profile_view_get(self):
        request = self.factory.get(reverse("delete-profile"))
        request.user = self.user
        response = views.DeleteProfile.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestHelp(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_password_view_get(self):
        request = self.factory.get(reverse("help"))
        response = views.Help.as_view()(request)
        self.assertEquals(response.status_code, 200)
