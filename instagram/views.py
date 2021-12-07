from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Image, UserProfile, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.
def landing(request):
    return render(request, 'landing.html')


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
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user

            if 'img' in request.FILES:
                new_post.image = request.FILES['img']

            new_post.save()   

        context = {
            'image_list':images,
            'form':form,
        }

        return render(request, 'index.html', context)   

class ImageDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)
        form = CommentForm() 

        comments = Comment.objects.filter(image = image).order_by('-created_on')

        context = {
            'image':image,
            'form':form,
            'comments':comments,
        }

        return render(request, 'image_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)
        form = CommentForm(request.POST) 
 
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.image = image
            new_comment.save()

        comments = Comment.objects.filter(image = image).order_by('-created_on')    

        context = {
            'image':image,
            'form':form,
            'comments':comments,
        }

        return render(request, 'image_detail.html', context)

class ImageEditView(UpdateView):
    model = Image
    fields = ['image_caption']

    template_name = 'image_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('image-detail', kwargs ={'pk':pk})

class ImageDeleteView(UpdateView):
    model = Image
    fields = ['image', 'author']
    template_name = 'image_delete.html'
    success_url = reverse_lazy('image-list')
 

class ProfileView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        images = Image.objects.filter(author = user).order_by('-created_on')   

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False    

        number_of_followers = len(followers)

        context = {
            'user':user,
            'profile':profile,
            'images':images,
            'number_of_followers':number_of_followers,
            'is_following':is_following,
        }        

        return render(request, 'profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['full_name', 'bio', 'profile_pic']
    template_name = 'profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk':pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user    

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk = profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk = profile.pk) 

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)

        for like in post.likes.all():
            if like == request.user:
                is_like = true
                break

            if not is_like:
                post.likes.add(request.user)
            if is_like:
                post.likes.remove(request.user)
        
class Dislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = true
                break

            if not is_like:
                post.likes.add(request.user)
            if is_like:
                post.likes.remove(request.user)

        return redirect('profile', pk = profile.pk)         

