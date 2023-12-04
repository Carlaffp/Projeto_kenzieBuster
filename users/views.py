from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUserOwner
from movies.permissions import IsMyCustomPermission



class LoginView(TokenObtainPairView):
    ...


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsAuthenticated, IsUserOwner]

    def get(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id) -> Response:
        found_user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, found_user)
        serilaizer = UserSerializer(found_user, data=request.data, partial=True)
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()
        return Response(serilaizer.data, status.HTTP_200_OK)
