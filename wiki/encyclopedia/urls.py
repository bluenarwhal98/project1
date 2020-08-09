from django.urls import path

from . import views


urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'^<str:title>/$', views.entry, name="entry"),
    path(r'^result/<str:query>/$', views.result, name="result"),
    path(r'^create/$', views.create, name="create"),
    path(r'^edit/<str:title>/$', views.edit, name="edit"),
]
