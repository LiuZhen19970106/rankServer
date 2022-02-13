
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
]
