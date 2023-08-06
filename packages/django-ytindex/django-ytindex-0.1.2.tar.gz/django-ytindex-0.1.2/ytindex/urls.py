from django.urls import path, re_path
from .views import search

urlpatterns = [
    re_path('/(?P<index>\w*)/(?P<query>.*)', search, name='ytindex-search'),
]
