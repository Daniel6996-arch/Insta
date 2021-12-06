from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from . import views
from .views import ImageListView, ImageDetailView, ImageEditView, ImageDeleteView, ProfileView

urlpatterns=[
    url('^$', views.landing, name='landing'),
    path('^profile/<int:pk>/', ProfileView.as_view(), name = 'profile'),
    url('^posts/',views.ImageListView.as_view(),name = 'image-list'),
    path('post/<int:pk>', ImageDetailView.as_view(), name = 'image-detail'),
    path('post/edit/<int:pk>', ImageEditView.as_view(), name = 'image-edit'),
    path('post/delete/<int:pk>', ImageDeleteView.as_view(), name = 'image-delete'),
]

