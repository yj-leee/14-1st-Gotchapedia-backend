import json
import requests

from django.views import View
from django.http  import JsonResponse

from .models         import Movie, MovieStaffPosition
from analysis.models import Star, Interest
from users.utils     import login_decorator

class SearchView(View):
    def get(self, request):
        search_key = request.GET.get('searchkey', None)
        queryset = MovieStaffPosition.objects.filter(Q(staff__name__icontains=search_key) | Q(movie__name__icontains=search_key))

        movielist = [{
            'name'     : movie.movie.name,
            'image'    : movie.movie.main_image,
            'country'  : movie.movie.country,
            'year'     : movie.movie.opening_at
        } for movie in queryset ]

        return JsonResponse({ 'result' : movielist }, status=200)

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

class InterestListView(View):
    @login_decorator
    def get(self, request):
        account_id = request.user
        status = request.GET.get('status')

        interests = Interest.objects.select_related('movie').prefetch_related('movie__star_set').filter(user_id=account_id)

        if status:
            interests = interests.filter(status=status)

        data = {
            'data': [{
                'movieId': interest.movie.id,
                'imageURL': interest.movie.main_image,
                'title': interest.movie.name,
                'rate': str(round(sum([star.point for star in interest.movie.star_set.all()])/interest.movie.star_set.all().count(),1)),
                'date': f'{interest.movie.opening_at.year} . {interest.movie.country}'
                } for interest in interests]
        }
        return JsonResponse(data, status=200)

class InterestView(View):
    @login_decorator
    def post(self, request, movie_id):
        data = json.loads(request.body)

        if 'status' not in data.keys():
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            return JsonResponse({"message": "ALREADY_EXIST"}, status=400)

        interest = Interest.objects.create(user_id=request.user, movie_id=movie_id, status=data["status"])

        context = {
            'id': interest.id,
            'status': interest.status
        }
        return JsonResponse(context, status=201)
    
    @login_decorator
    def get(self, request, movie_id):

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        context = {}
        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            interest = Interest.objects.get(user_id=request.user, movie_id=movie_id)
            context = {
                'id': interest.id,
                'status': interest.status
            }
        return JsonResponse(context, status=200)
    
    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        if 'status' not in data.keys():
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({'message': 'NO_MOVIE'}, status=400)

        if not Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            return JsonResponse({'message': 'NO_INTEREST'}, status=400)

        interest = Interest.objects.get(user_id=request.user, movie_id=movie_id)
        interest.status = data['status']
        interest.save()
        context = {
            'id': interest.id,
            'status': interest.status
        }
        return JsonResponse(context, status=200)

    @login_decorator
    def delete(self, request, movie_id):

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({'message': 'NO_MOVIE'}, status=400)

        interest = Interest.objects.filter(user_id=request.user, movie_id=movie_id)
        interest.delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)