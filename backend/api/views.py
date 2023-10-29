# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import logout
from rest_framework_jwt.settings import api_settings
from .models import User, Client, Freelancer
from .serializers import UserRegistrationSerializer, UserLoginSerializer,ClientProfileSerializer

@api_view(['POST'])
def client_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']

            # Check if the name is already taken
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Name is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def freelancer_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']

            # Check if the name is already taken
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Name is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([])
def client_login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_client:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response({'token': token, 'user_type': 'client'})
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def freelancer_login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_freelancer:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                client_profile_url = reverse('client-profile')  
                print(user)
                return Response({'token': token, 'user_type': 'freelancer', 'client_profile_url': client_profile_url})
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT','POST'])
@permission_classes([])
def client_profile(request):
    # Get the current client user
    client = Client.objects.get(user=request.user)

    if request.method == 'GET':
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data)
    
    
    if request.method == 'POST':
        serializer = ClientProfileSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = ClientProfileSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})