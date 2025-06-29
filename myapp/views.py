import secrets
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, viewsets, request
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import PasswordEntry
from .serializers import UserSerializer, PasswordEntriesSerializer, PasswordEntryListSerializer
from .utils import decrypt_password


# Create your views here.

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        # Ensure the user is authenticated
        if response.status_code == status.HTTP_200_OK:
            user = self.get_user(request.data)
            serializer = UserSerializer(user)
            response.data['user'] = serializer.data

        return Response(response.data, status=response.status_code)
    def get_user(self, data):
        username = data.get('username') or data.get('email')  # Adjust based on your login field
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValueError("Invalid credentials")
        return user

class PasswordEntriesViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordEntriesSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return PasswordEntryListSerializer
        return PasswordEntriesSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = "created entry succesfully"
        return response

class PasswordEntryListView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self, request):
        site_name = request.data.get('site_name')

        if not site_name:
            return Response({'error': 'site_name is required'}, status=status.HTTP_400_BAD_REQUEST)

        entry = get_object_or_404(PasswordEntry, site_name=site_name, user=request.user)

        try:
            decrypted_password = decrypt_password(entry.password, entry.iv)
            return Response({'decrypted_password': decrypted_password}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': 'decryption failed '+ str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GeneratePasswordView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request):
        password_length=13
        generated_password = secrets.token_urlsafe(password_length)
        return Response(generated_password, status=status.HTTP_200_OK)

