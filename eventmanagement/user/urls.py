from django.contrib import admin
from django.urls import path, include
from .views import register, get_users,login, logout, create_event, edit_event, delete_event, get_events, event_detail, book_tickets, my_bookings, filter_events, my_events

urlpatterns = [
    path('register/',register,name='register' ),
    path('dummy/', get_users),
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout'),
    path('create_event/', create_event, name= 'create_event'),
    path('edit_event/<int:event_id>/', edit_event, name= 'edit_event'),
    path('delete_event/<int:event_id>/', delete_event, name= 'delete_event'),
    path('get_events/', get_events, name= 'get_events'),
    path('event/<int:event_id>/', event_detail, name= 'event_detail'),
    path('book-event/<int:event_id>/',book_tickets , name= 'book_tickets'),
    path('my_bookings/',my_bookings , name= 'my_bookings'),
    path('events/filter/',filter_events , name= 'filter_events'),
    path('my_events/',my_events , name= 'my_events')
]

