from django.shortcuts import render
from django.views import View
from .models import Image
from .forms import PostForm

# Create your views here.
class ImageListView(View):
    def get(self, request):
        images = Image.objects.all().order_by('-created_on')
        form = PostForm()
        context = {
            'image_list':images,
            'form':form,
        }

        return render(request, 'index.html', context) 