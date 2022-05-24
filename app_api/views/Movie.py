from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from app_api.models import Movie
from django.db.models import Q
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
        pass

    def update(self, request, pk):
        pass

    def destroy(self, request, pk):
        pass

class MovieSerializer(serializers.ModelSerializer):
    """this will serialize data for movie views"""
    class Meta:
        model = Movie
        fields = ('title', 'description', 'run_time', 'user', 'date_released', 'genre')
        depth = 1
