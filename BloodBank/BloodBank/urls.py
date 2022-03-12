from django.contrib import admin
from django.urls import path , include
from . import views
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('contactus', views.contact),
    path('saveuser', views.saveuser),
    path('verifyuser', views.verifyuser),

    path('contact/',include('contact.urls')),
    path('myuser/',include('user.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
