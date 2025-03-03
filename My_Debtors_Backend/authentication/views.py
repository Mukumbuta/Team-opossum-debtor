from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response 
from .serializers import UserSerializer, LoginSerializer
from django.conf import settings
from django.contrib import auth
import jwt 


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)
            serializer = LoginSerializer(user)
            data = {
                'user': serializer.data,
                'token': auth_token
            }

            return Response({'Data': data}, status=status.HTTP_200_OK)
        return Response({'Error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
