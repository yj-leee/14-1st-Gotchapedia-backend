import json

from django.views import View
from django.http import JsonResponse

from .models import (
    Movie,
    Picture,
    Staff,
    MovieStaffPosition,
    Genre,
    MovieGenre
)

from users.models import User
from analysis.models import (
    Star,
    Interest
)

class MovieInfoView(View):
    #<-- login decorator -->
    def get(self, request, movieId):

        movie_info       = Movie.objects.filter(id=movieId)
        movie_genre      = MovieGenre.objects.filter(movie_id=movieId)
        movie_staff      = MovieStaffPosition.objects.filter(movie_id=movieId)
        movie_sub_image  = Picture.objects.filter(movie_id=movieId)

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

        staff_list = []
        if movie_staff.exists():
            staff_list = [{
                "name": staff.staff.name,
                "image": staff.staff.proflie_image,
                "position": staff.position.name
            }for staff in movie_staff]
        else:
            staff_list = []

        sub_image = []
        if movie_sub_image.exists():
            sub_image = [{
                "url": image.url
            }for image in movie_sub_image]
        else:
            sub_image = []

        feedback = {
                "id"          : movie.pk,
                "name"        : movie.name,
                "country"     : movie.country,
                "description" : movie.description,
                "mainImage"   : movie.main_image,
                "openDate"    : movie.opening_at.year,
                "showTime"    : movie.show_time,
                "genre"       : genre_list,
                "staff"       : staff_list,
                "subImage"    : sub_image
        }
        return JsonResponse({"data":feedback}, status=200)
