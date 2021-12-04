from django.db import models
import datetime as dt
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from PIL import Image
import PIL.Image as Image

# Create your models here.
#Image
#Image Name.
#Image Caption.
#Profile Foreign key
#Likes
#Comments


class Image(models.Model):
    image = models.ImageField(upload_to = 'images/', default)
