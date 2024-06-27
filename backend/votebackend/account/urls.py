from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [ 

    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_create'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]