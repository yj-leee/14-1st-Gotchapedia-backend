import json

from django.views import View
from django.http  import JsonResponse

from .models      import Movie, Genre, MovieGenre
from users.models import User
from users.utils  import login_decorator

class MovieDetailView(View):
    @login_decorator
    def get(self, request, movie_id):

        movie_info = Movie.objects.prefetch_related('moviegenre_set').get(id=movie_id)

        feedback = {
                "name"        : movie_info.name,
                "country"     : movie_info.country,
                "description" : movie_info.description,
                "openDate"    : movie_info.opening_at.year,
                "showTime"    : movie_info.show_time,
                "genre"       : [{"name": genre.genre.name
                                 }for genre in movie_info.moviegenre_set.select_related('genre')]
        }

        return JsonResponse({"data":feedback}, status=200)
