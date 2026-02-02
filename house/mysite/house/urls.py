from django.urls import path, include
from.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user_profile', UserProfileViewSet, basename='user_profile'),
router.register(r'property', PropertyViewSet, basename='property'),
router.register(r'review', ReviewViewSet, basename='reviews'),


urlpatterns =[
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('predict/', PredictPrice.as_view(), name='predict_price')
]