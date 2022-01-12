from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('text', views.add_text),
    path('text/text', views.search_from_index),
]
