from django.db import models
from django.urls import reverse

from category.models import Category
from ckeditor.fields import RichTextField
from accounts.models import Account


# Create your models here.
class Post(models.Model):
    topic = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    sub_topic = models.CharField(max_length=255)
    body = RichTextField(null=True, blank=True)
    phone_nmumber = models.CharField(max_length=20)
    body = models.TextField()
    images = models.ImageField(upload_to ='photos/posts', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_url(self):
        return reverse('post_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.topic

class ReviewRating(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     user = models.ForeignKey(Account, on_delete=models.CASCADE)
     subject = models.CharField(max_length=255, blank=True)
     review = models.TextField(max_length=500, blank=True)
     rating = models.FloatField()
     ip = models.CharField(max_length=255, blank=True)
     status = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return self.subject



   
