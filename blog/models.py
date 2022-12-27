from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    # objects is the default manager.
    objects = models.Manager()
    # published is the custom manager added to retrieve queryset filtered by status = 'published' filter.
    published = PublishedManager()

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
    
    def __str__(self):
        return self.title






