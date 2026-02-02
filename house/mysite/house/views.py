from rest_framework import viewsets, generics, views
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter, TypeFilter
from .paginations import HousePagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import CreateReview
import joblib
from django.conf import settings
import os

model_path = os.path.join(settings.BASE_DIR, 'model-m.pkl')
model = joblib.load(model_path)

vec_m_path = os.path.join(settings.BASE_DIR, 'vec_m.pkl')
vec_m = joblib.load(vec_m_path)


Neighborhoods = [
    'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards',
    'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes',
    'NoRidge', 'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst',
    'StoneBr', 'Timber', 'Veenker'
]


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail':' неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter, TypeFilter
    search_fields = ['title']
    ordering_fields = ['created_date', 'area', 'price']
    pagination_class = HousePagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CreateReview]


class PredictPrice(views.APIView):
    def post(self, request):
        instance = HousePredictSerializer(data=request.data)
        if instance.is_valid():
            data = instance.validated_data

            # dict -> list of values
            features = list(data.values())

            # векторизация/масштабдоо
            transformed = vec_m.transform([features])

            # предикт
            pred = model.predict(transformed)[0]

            return Response({'HousePrice': pred}, status=status.HTTP_200_OK)

        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)
