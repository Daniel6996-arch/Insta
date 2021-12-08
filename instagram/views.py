from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Image, UserProfile, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/')
def users(request):
    users = UserProfile.objects.all()
    
    return render(request, 'welcome.html', {'users':users})      

def search(request):

    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_users = UserProfile.search_user(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"users":searched_users})

    else:
        return render(request, 'search.html', {"message":message})     


class ImageListView(View):
    def get(self, request):
        images = Image.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'image_list':images,
            'form':form,
        }

        return render(request, 'image-list.html', context) 


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

        return render(request, 'image-list.html', context)   

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

        is_dislike = False

        for dislike in image.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            image.dislikes.remove(request.user)        

        is_like = False

        for like in image.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            image.likes.add(request.user)
        if is_like:
            image.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


                
        
class Dislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        image = Image.objects.get(pk=pk)

        is_like = False

        for like in image.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            image.likes.remove(request.user)         

        is_dislike = False

        for dislike in image.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            image.dislikes.add(request.user)
        if is_dislike:
            image.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


                        

