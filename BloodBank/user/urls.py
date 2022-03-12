from django.urls import path 
from . import views

urlpatterns = [ 
    path('home', views.home),
    path('request', views.bloodrequest),
    path('saverequest', views.saverequest),
    path('profile', views.profile),
    path("uploadpic",views.uploadpic),
    path('changepassword',views.changepassword),
    path('logout', views.logout),
]
