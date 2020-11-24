import json
import requests

from django.views    import View
from django.http     import JsonResponse

from .models         import (
    Movie,
    Picture,
    Staff,
    MovieStaffPosition,
    Genre,
    MovieGenre
)
from .models         import Staff
from users.models    import User
from analysis.models import Star
from users.utils     import login_decorator


class SearchView(View):
    def get(self, request):
        search_key = request.GET.get('searchkey',None)
        if Movie.objects.filter(name__icontains=search_key).exists():
            moviequeryset = Movie.objects.filter(name__icontains=search_key)
            movielist = []
            for movie in moviequeryset:
               movielist.append({
                    'name'     : movie.name,
                    'image'    : movie.main_image,
                    'country'  : movie.country,
                    'year'     : movie.opening_at
               })
            return JsonResponse({'result': movielist}, status=200)

        elif Staff.objects.filter(name__icontains=search_key).exists():
            moviequeryset = Staff.objects.filter(name__icontains=search_key)
            movielist = []
            for moviequery in moviequeryset:
                for movie in moviequery.movie.all():
                    movielist.append({
                        'name'     : movie.name,
                        'country'  : movie.country,
                        'year'     : movie.opening_at
                    })
            return JsonResponse({'result' : movielist}, status=200)
        else:
            return JsonResponse({'result' : None}, status=400)
          

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
    @login_decorator
    def get(self, request, movie_id):

        movie_info = Movie.objects.prefetch_related('moviegenre_set',
                                                    'picture_set',
                                                    'moviestaffposition_set').get(id=movie_id)

        feedback = {
            "id"          : movie_info.pk,
            "name"        : movie_info.name,
            "country"     : movie_info.country,
            "description" : movie_info.description,
            "mainImage"   : movie_info.main_image,
            "openDate"    : movie_info.opening_at.year,
            "showTime"    : movie_info.show_time,
            "genre"       :[{"name": genre.genre.name
                            }for genre in movie_info.moviegenre_set.select_related('genre')],
            "staff"       :[{"name": staff.staff.name,
                             "image": staff.staff.proflie_image,
                             "position": staff.position.name
                            }for staff in movie_info.moviestaffposition_set.select_related('staff', 'position')],
            "subImage"    :[{"url": image.url
                            }for image in movie_info.picture_set.all()]
        }

        return JsonResponse({"data":feedback}, status=200)