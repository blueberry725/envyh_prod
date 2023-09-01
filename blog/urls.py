# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_view, name='category_view'),
]
