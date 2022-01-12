from django.contrib import admin
from django.urls import path
from . import views, odb


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('add-text/', odb.add_text),
    path('text', odb.search_from_index),
]
