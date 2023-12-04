from rest_framework.views import APIView, Request, Response, status
from movies_orders.models import MovieOrder
from movies.models import Movie
from movies_orders.serializers import MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id)-> Response:
        found_movie = get_object_or_404(Movie, pk=movie_id)
        user = request.user
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, movie=found_movie)
        return Response(serializer.data, status.HTTP_201_CREATED)

