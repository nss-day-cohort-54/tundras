from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from app_api.models import Movie, Genre
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
class MovieView(ViewSet):

    def list(self, request):
        """List Movie View"""
        genre = self.request.query_params.get("genre", None)
        search = request.query_params.get('search', None)

        if genre != None:
            movies = Movie.objects.filter(genre__name = genre)
            # where genre.name = genre
            # vs
            # where genre.id = genre
        elif search is not None:
            movies = Movie.objects.filter(Q(title__contains = search)| Q(description__contains = search))
        else:
            movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def create(self, request):
        """create"""
        user = request.auth.user

        movie = CreateMovieSerializer(data = request.data)

        movie.is_valid(raise_exception = True)

        movie.save(user = request.auth.user)


        # genre = Genre.objects.get(pk=request.data['genre'])
        # movie = Movie.objects.create(
        #     user=user, genre=genre,
        #     title = request.data['title']


        #     description = request.data['description'],
        #     run_time = request.data['run_time'],
        #     date_released = request.data['date_released']
        # )
        # serializer = MovieSerializer(movie)

        return Response(movie.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        
        movie = Movie.objects.get(pk = pk)
        serializer = CreateMovieSerializer(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.auth.user)

        return Response(None, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=False)
    def my_movies(self, request):
        """Return movies of the current user"""

        user = request.auth.user
        movies = Movie.objects.filter(user=user)
        serialized = MovieSerializer(movies, many=True)
        return Response(serialized.data)

class CreateMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model= Movie
        fields= ('title', 'description', 'run_time', 'date_released', 'genre')
class MovieSerializer(serializers.ModelSerializer):
    """this will serialize data for movie views"""
    class Meta:
        model = Movie
        fields = ('title', 'description', 'run_time', 'user', 'date_released', 'genre')
        depth = 1
