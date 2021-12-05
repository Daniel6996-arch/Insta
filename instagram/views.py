from django.shortcuts import render
from django.Views import Views
from .models import Image


# Create your views here.
def index(self, request):
    images = Image.objects.all().order_by('-created_on')
    
    context = {
        'image_list':images,
    }

    return render(request, 'index.html', context) 