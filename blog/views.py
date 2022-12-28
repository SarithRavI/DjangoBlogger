from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import FormComment

def list_view(request):
    posts = Post.published.all()
    return render(request,   # request object
                 'blog/post/list.html',  # path to template from the template root
                 {'posts':posts} # context
                 )  

def detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,
                            status='published',
                            publish__year = year,
                            publish__month = month,
                            publish__day = day)
    # get all the comments. 
    # here we utilize the related_name defined in the Comment model to Post foreign key.                        
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = FormComment(data = request.POST)
        if comment_form.is_valid():
            # create a new instance
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = FormComment()

    # return render(request,'blog/post/detail.html',
    #              {'post':post})

    return render(request,'blog/post/detail.html',
                 {'post':post,
                 'comments':comments,
                 'comment_form':comment_form,
                 'new_comment':new_comment})
