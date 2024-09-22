from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Event, User
from django.utils import timezone
from django.urls import reverse

# Create your tests here.

class EventAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "testuser@example.com",
            password = "password123",
            username = "Test123",
            name = "Test User",
            role = "manager",
        )
        # self.event =  Event.objects.create(
        #     title = "Event 2",
        #     description = "Description of the event",
        #     date ="2023-09-30T10:00:00Z",
        #     time = "15:00:00",
        #     location="Bangalore",
        #     total_tickets = 50,
        #     tickets_sold =10,
        #     created_by = self.user
        # )

        Event.objects.create(
            title = "Event 1",
            description = "Description of the event",
            date ="2023-09-30T10:00:00Z",
            time = "15:00:00",
            location="Bangalore",
            total_tickets = 50,
            tickets_sold =10,
            created_by = self.user
        )
        
        self.client = APIClient()
        self.client.login(email="testuser@example.com", password = "password123")

    def authenticate(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'testuser@example.com', 'password':"password123"},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+response.data['access_token'])

    def test_create_event(self):
        self.authenticate()
        data = {
            "title":"New Event",
            "description": "Event Description",
            "date": timezone.now(),
            "time":timezone.now().time(),
            "location":"Bangalore",
            "total_tickets":50,
        }
        response = self.client.post(reverse('create_event'),data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.first().created_by, self.user)

    def test_get_events(self):
        self.authenticate()
        response = self.client.get(reverse('get_events'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
    
    def test_filter_events_by_location(self):
        self.authenticate()
        response = self.client.get(reverse('filter_events')+ '?location=Bangalore')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['location'],'Bangalore')
    
    def test_book_event(self):
        self.authenticate()
        url = reverse('book_tickets', kwargs = {'event_id' : 2})
        data={
            "number_of_tickets": 1
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    