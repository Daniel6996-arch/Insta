from django.db import models
import datetime as dt
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from PIL import Image
import PIL.Image as Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# Create your models here.
class Image(models.Model):
    image = CloudinaryField('image')
    image_name = models.CharField(max_length = 60)
    image_caption = models.TextField(blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

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
    full_name = models.CharField(max_length=30)
    bio = HTMLField(blank=True, null=True)
    profile_pic = CloudinaryField('image')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User) 
def save_user_Profile(sender, instance, **kwargs):
    instance.profile.save()        
        