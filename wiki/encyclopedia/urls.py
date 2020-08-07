from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path(r"^<str:title>/$", views.entry, name="entry"),
    path(r"result/^<str:query>$", views.result, name="result"),
]
