from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post

def list_view(request):
    posts = Post.published.all()
    return render(request,   # request object
                 'blog/post/list.html',  # path to template from the template root
                 {'posts':posts} # context
                 )  