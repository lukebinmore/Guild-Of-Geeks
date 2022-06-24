from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:slug>/', views.Post.as_view(), name='post')
]