from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('Dept/<str:DName>', views.dept),
    path('course/<str:CCode>', views.Crs),
    path('signup', views.signup),
    path('logout', views.logout),
    path('login', views.login),
    path('uploader/<str:CCode>', views.uploader),
    path('contact', views.contact),
    path('feedback', views.feedback),
    path('crssrch', views.crssrch),
    path('deprequest', views.deprequest),
]
