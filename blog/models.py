from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    # objects is the default manager.
    objects = models.Manager()
    # published is the custom manager added to retrieve queryset filtered by status = 'published' filter.
    published = PublishedManager()
    tags = TaggableManager()

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
        )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # doc: https://docs.djangoproject.com/en/3.2/ref/models/fields/#choices
    status = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='draft')
    
    class Meta:
        ordering = ('-publish',)

    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                      args = (self.publish.year,
                      self.publish.month,
                      self.publish.day,
                      self.slug))
    
    def __str__(self):
        return self.title

class Comment(models.Model):

    post = models.ForeignKey(to = Post,
                             on_delete=models.CASCADE,
                             related_name= 'comments')
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    text = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('publish',)
    
    def __str__(self):
        return f"Commet for post {self.post.pk} by {self.name}"



