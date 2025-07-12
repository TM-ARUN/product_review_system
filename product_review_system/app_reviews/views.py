from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from .models import *
from .serializers import *

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            Token.objects.create(user = user)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user = user)
        return Response({
            'token':token.key,
            'user_id': user.pk,
            'is_admin': user.is_admin
        })
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

# for product

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        if not self.request.user.is_admin:
            return Response(
                {"details":"Only admin users can create products"},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer.save(created_by = self.request.user)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        if not self.request.user.is_admin:
            return Response(
                {"details": "Only admin users can update products"},
                status= status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        if not self.request.user.is_admin:
            return Response(
                {"detail": "Only admin users can delete products."},
                status= status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        
            