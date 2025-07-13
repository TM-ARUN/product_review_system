from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Force password hashing - NO EXCEPTIONS
        validated_data['password'] = make_password(validated_data['password'])
        
        # DEBUG: Print the hashed password before saving
        print(f"Hashing password. Result: {validated_data['password']}")
        
        # Use get_or_create to prevent duplicates
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={
                'email': validated_data['email'],
                'password': validated_data['password'],
                'is_admin': validated_data.get('is_admin', False)
            }
        )
        
        if not created:
            user.password = validated_data['password']
            user.save()
        
        return user
class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id','name','description', 'price', 'created_by', 'average_rating', 'review_count', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'average_rating', 'review_count']
        
    def get_average_rating(self,obj):
        return obj.average_rating()
    def get_review_count(self,obj):
        return obj.reviews.count()
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'feedback', 'created_at', 'updated_at']
        read_only_fields = ['user', 'product']
    
    def validate_rating(self,value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating should be between 1 and 5")
        return value