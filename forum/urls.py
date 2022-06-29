from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:slug>/', views.PostView.as_view(), name='post-view'),
    path('edit/<slug:slug>/', views.PostEdit.as_view(), name='post-edit')
]