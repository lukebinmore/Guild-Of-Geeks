from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:slug>/', views.PostView.as_view(), name='post-view'),
    path('edit/<slug:slug>/', views.PostEdit.as_view(), name='post-edit'),
    path('post-like/<slug:slug>/', views.PostLike.as_view(), name='post-like'),
    path('comment-like/<int:id>/', views.CommentLike.as_view(), name='comment-like'),
    path('accounts/login-signup/', views.LoginSignup.as_view(), name='login-signup')
]