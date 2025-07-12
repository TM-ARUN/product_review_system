from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_admin']
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