from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('login/',CustomAuthToken.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('products/',ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/',ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    
]