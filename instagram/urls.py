from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from . import views
from .views import ImageListView, ProfileView

urlpatterns=[
    path('^profile/<int:pk>/', ProfileView.as_view(), name = 'profile'),
    url('',views.ImageListView.as_view(),name = 'image-list'),
    

]

