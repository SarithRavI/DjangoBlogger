from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
        )

    title = models.CharField()
    slug = models.SlugField()
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
        ordering = ('-publish')
    
    def __str__(self):
        return self.title
