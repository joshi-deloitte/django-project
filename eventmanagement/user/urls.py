from django.contrib import admin
from django.urls import path, include
from .views import register, get_users,login, logout, create_event, edit_event, delete_event, get_events

urlpatterns = [
    path('register/',register,name='register' ),
    path('dummy/', get_users),
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout'),
    path('create_event/', create_event, name= 'create_event'),
    path('edit_event/<int:event_id>/', edit_event, name= 'edit_event'),
    path('delete_event/<int:event_id>/', delete_event, name= 'delete_event'),
    path('get_events/', get_events, name= 'get_events')
]

