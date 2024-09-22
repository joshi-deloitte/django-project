from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Event
from django.contrib.auth import get_user_model
from .permission import IsManager
from .serializers import RegisterSerilaizer,LoginSerializer, EventSerializer

# Create your views here.

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        return Response(User.objects.all()[1].password)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token' : str(refresh)
                }, status = status.HTTP_200_OK)
                
            else:
                return  Response({"error":"Already Logged in"}, status= status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error":"Invalid credentials"}, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        print(request.user.is_authenticated)
        return Response({"message: successfully logged out"}, status= status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status = status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([IsManager])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_authenticated:
            serializer.save(created_by = request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsManager])
def edit_event(request,event_id):
    try:
        event = Event.objects.get(id=event_id, created_by=request.user)
    except Event.DoesNotExist:
        return Response({"error": "event not found or you are not authorized to edit this event"},status=status.HTTP_400_BAD_REQUEST)
    
    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
         

@api_view(['DELETE'])
@permission_classes([IsManager])
def delete_event(request,event_id):
    try:
        event = Event.objects.get(id=event_id, created_by=request.user)
    except Event.DoesNotExist:
        return Response({"error": "event not found or you are not authorized to delete this event"},status=status.HTTP_400_BAD_REQUEST)
    
    event.delete()
    return Response({"message":"event deleted successfully"},status= status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
    try:
        events = Event.objects.all()
        serializer = EventSerializer(events, many= True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({"error": "event not found or you are not authorized to get this event"},status=status.HTTP_400_BAD_REQUEST)
         
    

        
        