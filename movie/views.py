import json

from django.views import View
from django.http  import JsonResponse

from .models      import Movie, Genre, MovieGenre
from users.models import User


class MovieDetailView(View):
    #<-- login decorator -->
    def get(self, request, movieId):

        movie_info       = Movie.objects.filter(id=movieId)
        movie_genre      = MovieGenre.objects.filter(movie_id=movieId)

        if movie_info.exists():
            movie =  movie_info.first()
        else:
            return JsonResponse({"message":"NO_MOVIE"}, status=404)

        genre_list = []
        if movie_genre.exists():
            gnere = movie_genre.first()
            genre_list = [{
                "name": gnere.genre.name
            } for ganre_name in movie_genre]
        else:
            genre_list = []

        feedback = {
                "name"        : movie.name,
                "contry"      : movie.contry,
                "description" : movie.description,
                "openDate"    : movie.opening_at.year,
                "showTime"    : movie.show_time,
                "genre"       : genre_list,
        }
        return JsonResponse({"data":feedback}, status=200)
