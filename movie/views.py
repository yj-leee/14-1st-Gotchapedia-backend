import json

from django.views import View
from django.http  import JsonResponse

from .models      import Movie, Genre, MovieGenre
from users.models import User
from analysis.models import Star
from users.utils  import login_decorator

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