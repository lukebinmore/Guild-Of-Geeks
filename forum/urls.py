from . import views
from .decorators import login_required
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:slug>/', views.PostView.as_view(), name='post-view'),
    path('post-edit/<slug:slug>/', login_required(views.PostEdit.as_view()), name='post-edit'),
    path('post-delete/<slug:slug>/', views.PostDelete.as_view(), name='post-delete'),
    path('post-like/<slug:slug>/', views.PostLike.as_view(), name='post-like'),
    path('post-follow/<slug:slug>/', views.PostFollow.as_view(), name='post-follow'),
    path('comment-like/<int:id>/', views.CommentLike.as_view(), name='comment-like'),
    path('comment-delete/<int:id>/', views.CommentDelete.as_view(), name='comment-delete'),
    path('category-follow/<int:id>/', views.CategoryFollow.as_view(), name='category-follow'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
    path('accounts/logout/', views.Logout.as_view(), name='logout'),
    path('accounts/profile/<str:mode>', login_required(views.Profile.as_view()), name='profile'),
    path('accounts/password/', views.UpdatePassword.as_view(), name='password'),
    path('accounts/delete-profile/', views.DeleteProfile.as_view(), name='delete-profile'),
    path('help/contact-us/', views.ContactUs.as_view(), name='contact-us'),
    path('help/information/', views.Help.as_view(), name='help')
]