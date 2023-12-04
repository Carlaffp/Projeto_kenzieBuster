from django.urls import path
from .views import UserView, UserDetailView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/login/', LoginView.as_view() ),
    path('users/login/refresh/', TokenRefreshView.as_view()),
    path('users/<int:user_id>/', UserDetailView.as_view())
]