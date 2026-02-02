from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = UserProfile.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Пользователь с таким email не найден")
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance. username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refresh')
        try:

            token = RefreshToken(refresh_token)
            return data
        except TokenError:
            raise serializers.ValidationError({'detail': 'Недействительный токен.'})

    def save(self):

        refresh_token = self.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id','username', 'email', 'first_name',  'last_name', 'phone_number', 'role','preferred_language',
            'date_joined','last_login','is_active', 'is_staff','is_superuser',
        ]


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_type
        fields = [
            'id',
            'property_name',
        ]


class ImagePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Property
        fields = [
            'id',
            'property_image',
        ]


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description','property_type','region', 'city','district','address','area', 'price',
            'rooms','floor','total_floors','condition','images', 'image', 'documents', 'document','seller', 'created_date',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id','author','seller', 'rating', 'comment','created_date',
        ]


class HousePredictSerializer(serializers.Serializer):
    GrLivArea = serializers.IntegerField()
    YearBuilt = serializers.IntegerField()
    GarageCars = serializers.IntegerField()
    TotalBsmtSF = serializers.IntegerField()
    FullBath = serializers.IntegerField()
    OverallQual = serializers.IntegerField()
    Neighborhood = serializers.CharField(max_length=50)
