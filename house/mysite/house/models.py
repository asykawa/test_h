from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator



class UserProfile(AbstractUser):
    USER_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('buyer', 'buyer')
    )
    phone_number = PhoneNumberField()
    role = models.CharField(max_length=10, choices=USER_CHOICES, default='seller')
    preferred_language = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.username}-{self.role}'


class Property_type(models.Model):
    property_name = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.property_name}'


class Image_Property(models.Model):
    property_image = models.ImageField(upload_to='property_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.property_image}'


class Property(models.Model):
    CONDITION_CHOICES = (
        ('new', 'new'),
        ('used', 'used'),
        ('needs_repair', 'needs_repair')
    )
    title = models.CharField(max_length=32)
    description = models.TextField()
    property_type = models.ForeignKey(Property_type, on_delete=models.CASCADE, related_name='property_type')
    region = models.CharField(max_length=44, null=True, blank=True)
    city = models.CharField(max_length=44, null=True, blank=True)
    district = models.CharField(max_length=32)
    address = models.CharField(max_length=44)
    area = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    rooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)], null=True, blank=True)
    floor = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)], null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)], null=True, blank=True)
    condition = models.CharField(max_length=55, choices=CONDITION_CHOICES, default='used')
    images = models.ForeignKey(Image_Property, on_delete=models.CASCADE, related_name='images')
    image = models.BooleanField()
    documents = models.FileField(upload_to='documents/')
    document = models.BooleanField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}-{self.property_type}'


class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_review')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_review')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)],
                                              null=True, blank=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}-{self.seller}'


class House(models.Model):
    GrLivArea = models.IntegerField()
    YearBuilt = models.IntegerField()
    GarageCars = models.IntegerField()
    TotalBsmtSF = models.IntegerField()
    FullBath = models.IntegerField()
    OverallQual = models.IntegerField()
    Neighborhood = models.CharField(max_length=50)
    predicted_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"House {self.id} - {self.predicted_price}"
