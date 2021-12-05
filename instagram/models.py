from django.db import models
import datetime as dt
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from PIL import Image
import PIL.Image as Image

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to = 'images/', default = 'SOME STRING')
    image_name = models.CharField(max_length = 60)
    image_caption = models.TextField(blank = True)
    creator_profile = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    likes = models.IntegerField()

class Comment(models.Model): 
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)


    class Meta: 
        ordering = ('created_on',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.author, self.created_on)     

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key = True, verbose_name = 'user', related_name = 'profile', on_delete = models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = HTMLField()
    profile_pic = models.ImageField(upload_to = 'images/profile_pics', default = 'images/profile_pics/default.jpg', blank = True)