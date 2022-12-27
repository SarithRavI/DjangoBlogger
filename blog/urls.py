from django.urls import path
from .views import list_view

app_name = 'blog'

urlpatterns = [
    path('',list_view,name = 'post_list'),
]
