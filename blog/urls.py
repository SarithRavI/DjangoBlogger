from django.urls import path
from .views import list_view,detail_view

app_name = 'blog'

urlpatterns = [
    path('',list_view,name = 'post_list'),
    path('tag/<slug:tag_slug>',list_view,name = 'post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',detail_view,name = 'post_detail'),
]
