from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("search/<str:q>", views.search, name="search"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),
    path("edit/<str:entry>", views.edit, name="edit")
]