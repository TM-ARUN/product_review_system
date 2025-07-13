from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="products")
    
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        total_rating = sum(review.rating for review in reviews)
        review_count = reviews.count()
        average = total_rating / review_count
        rounded_average = round(average,1)
        return rounded_average
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product','user')
    def __str__(self):
        return f"{self.user.username} 's review for {self.product.name}"
    

