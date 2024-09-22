from rest_framework import serializers
from .models import Event, Booking
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email','username','name','password','role')

    def create(self,validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            name = validated_data['name'],
            password= validated_data['password'],
            role = validated_data['role'],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'],password = data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title','description','date','time','location','total_tickets','tickets_sold','tickets_available','created_by','category']
        read_only_fields = ['created_by','tickets_available']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','event','number_of_tickets','booking_date']
 