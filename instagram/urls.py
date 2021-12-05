from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from .views import ImageListView

urlpatterns=[
    url('',views.ImageListView.as_view(),name = 'image-list'),
    
]

