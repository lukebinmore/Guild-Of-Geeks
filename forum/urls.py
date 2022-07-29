from . import views
from .decorators import (
    login_required,
    check_comment_author,
    check_post_author,
    check_ajax,
)
from django.urls import path

# A list of url patterns.
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("<slug:slug>/", views.PostView.as_view(), name="post-view"),
    path(
        "post-edit/<slug:slug>/",
        login_required(check_post_author(views.PostEdit.as_view())),
        name="post-edit",
    ),
    path(
        "post-delete/<slug:slug>/",
        check_post_author(check_ajax(views.PostDelete.as_view())),
        name="post-delete",
    ),
    path("post-like/<slug:slug>/", views.PostLike.as_view(), name="post-like"),
    path(
        "post-follow/<slug:slug>/",
        views.PostFollow.as_view(),
        name="post-follow",
    ),
    path(
        "comment-like/<int:id>/",
        views.CommentLike.as_view(),
        name="comment-like",
    ),
    path(
        "comment-delete/<int:id>/",
        check_comment_author(check_ajax(views.CommentDelete.as_view())),
        name="comment-delete",
    ),
    path(
        "category-follow/<int:id>/",
        views.CategoryFollow.as_view(),
        name="category-follow",
    ),
    path("accounts/login/", check_ajax(views.Login.as_view()), name="login"),
    path(
        "accounts/signup/", check_ajax(views.Signup.as_view()), name="signup"
    ),
    path("accounts/logout/", views.Logout.as_view(), name="logout"),
    path(
        "accounts/profile/<str:mode>",
        login_required(views.Profile.as_view()),
        name="profile",
    ),
    path(
        "accounts/password/",
        login_required(check_ajax(views.UpdatePassword.as_view())),
        name="password",
    ),
    path(
        "accounts/delete-profile/",
        login_required(check_ajax(views.DeleteProfile.as_view())),
        name="delete-profile",
    ),
    path("help/contact-us/", views.ContactUs.as_view(), name="contact-us"),
    path("help/information/", views.Help.as_view(), name="help"),
]
