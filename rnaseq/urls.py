from django.urls import path
from . import views

urlpatterns = [
    path('rnaseq/', views.geneidfunc, name='rnaseq'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.logoutfunc, name='logout'),
]