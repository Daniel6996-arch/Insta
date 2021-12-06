from django.shortcuts import render
from django.views import View
from .models import Image, UserProfile
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


    def post(self, request):
        images = Image.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()   

        context = {
            'image_list':images,
            'form':form,
        }

        return render(request, 'index.html', context)   


class ProfileView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        images = Image.objects.filter(author = user).order_by('-created_on')   

        context = {
            'user':user,
            'profile':profile,
            'images':images,
        }        

        return render(request, 'profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'profile_pic']
    template_name = 'profile_edit'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk':pk})

    def test_func(self):
    profile = self.get_object()
    return self.request.user == profile.user    