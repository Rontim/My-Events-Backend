from django.urls import path
from .views import (CustomTokenObtainPairView,
                    CustomTokenRefreshView,  CustomTokenVerifyView, Logout)


urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', Logout.as_view(), name='logout'),
]
