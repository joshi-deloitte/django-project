from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth import get_user_model
from .serializers import RegisterSerilaizer,LoginSerializer

# Create your views here.

User = get_user_model()

@api_view(['POST'])
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
        return Response({"message: successfully logged out"}, status= status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status = status.HTTP_400_BAD_REQUEST)

    

        
        