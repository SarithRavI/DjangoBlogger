from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.db.models import Count 
from .models import Post
from taggit.models import Tag
from .forms import FormComment


def list_view(request,tag_slug = None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        # if we  use filter tags = tag 
        # we implicity say tag object has multiple tags inside.
        object_list = object_list.filter(tags__in = [tag])
    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blog/post/list.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag})

def detail_view(request,year,month,day,post):
    limit = request.GET.get('limit',None)
    post = get_object_or_404(Post,slug=post,
                            status='published',
                            publish__year = year,
                            publish__month = month,
                            publish__day = day)
    tags = post.tags.all()
    similar_posts = Post.published.filter(tags__in = tags).exclude(id=post.id).distinct()
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')
    if limit:
        similar_posts = similar_posts[:limit]
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
                 'new_comment':new_comment,
                 'similar_posts':similar_posts})
