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

class ReadMovieInfoView(View):
    #<-- login decorator -->
    def get(self, request):
        movie  = request.GET.get('movieId')

        if 'movieId' not in request.GET:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        movie_info       = Movie.objects.filter(id=int(movie))
        movie_genre      = MovieGenre.objects.filter(movie_id=int(movie))
        movie_staff      = MovieStaffPosition.objects.filter(movie_id=int(movie))
        movie_sub_image  = Picture.objects.filter(movie_id=int(movie))

        if movie_info.exists():
            movie =  movie_info.first()
        else:
            return JsonResponse({"message":"NO_MOVIE"}, status=404)

        genre_list = []
        if movie_genre.exists():
            gnere = movie_genre.first()
            genre_list = [{
                "name":gnere.genre.name
            } for ganre_name in movie_genre]
        else:
            genre_list = []

        staff_list = []
        if movie_staff.exists():
            staff_list = [{
                "staffName": staff.staff.name,
                "staffImage": staff.staff.proflie_image,
                "staffPosition": staff.position.name
            }for staff in movie_staff]
        else:
            staff_list = []

        sub_image = []
        if movie_sub_image.exists():
            sub_image = [{
                "image_url": image.url
            }for image in movie_sub_image]
        else:
            sub_image = []

        feedback = {
                "movieId"          : movie.pk,
                "movieName"        : movie.name,
                "movieContry"      : movie.contry,
                "movieDescription" : movie.description,
                "movieMainImage"   : movie.main_image,
                "movieOpenDate"    : movie.opening_at.year,
                "movieShowTime"    : movie.show_time,
                "movieGenre"       : genre_list,
                "moviestaff"       : staff_list,
                "movieSubImage"    : sub_image
        }
        return JsonResponse(feedback, status=200)
