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
from analysis.models import Star

class MoviesUserView(View):
    def get(self, request):
        account_id = request.GET.get('id')

        try:
            if account_id:
                stars = Star.objects.select_related('movie').filter(user_id=int(account_id)).order_by('-point')
            else:
                stars = Star.objects.select_related('movie').all().order_by('-point')

            context = {
                'data': [{
                    'movieId': star.movie.id,
                    'imageURL': star.movie.main_image,
                    'title': star.movie.name,
                    'rate': star.point,
                    'date': f'{star.movie.opening_at.year} . {star.movie.country}'
                 } for star in stars]
            }
            return JsonResponse(context, status=200)
        except ValueError:
            return JsonResponse({'message': 'INSTANCE_IS_NOT_NUMBER'}, status=400)

          
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

        genre_list = [{"name": gnere.genre.name} for genre in movie_genre if movie_genre.exists()]

        staff_list = [{
            "name": staff.staff.name,
            "image": staff.staff.proflie_image,
            "position": staff.position.name
        }for staff in movie_staff if movie_staff.exists()]

        sub_image = [{"url": image.url}for image in movie_sub_image if movie_sub_image.exists()]

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