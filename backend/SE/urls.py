from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("get_all_keywords", views.get_all_keywords, name="keywords"),
]