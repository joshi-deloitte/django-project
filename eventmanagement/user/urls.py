from django.contrib import admin
from django.urls import path, include
from .views import register, get_users,login, logout

urlpatterns = [
    path('register/',register,name='register' ),
    path('dummy/', get_users),
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout')
]

