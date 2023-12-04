from rest_framework.views import APIView, status, Request, Response
from movies.models import Movie
from movies.serializers import MovieSerilaizer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsMyCustomPermission
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsMyCustomPermission]

    def post(self, request: Request) -> Response:
        serializer = MovieSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user) 
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerilaizer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsMyCustomPermission]

    def get(self, request: Request, movie_id) -> Response:
        found_movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerilaizer(found_movie)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request: Request, movie_id) -> Response:
        found_movie = get_object_or_404(Movie, pk=movie_id)
        found_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
