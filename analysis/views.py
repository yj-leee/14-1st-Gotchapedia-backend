import json
import jwt
import requests
import numpy

from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.db.models import  Count, Avg

from users.models import User
from users.utils import login_decorator
from movie.models import Movie
from .models import Star

class FavoriteView(View):
    @login_decorator
    def get(self, request):
        account_id = request.user
        category   = request.GET.get('category', 'genre') # '장르(genre)' 또는 '국가(country)'

        stars = []
        category_path = ''

        if category == 'genre':
            stars = Star.objects.select_related('movie').prefetch_related('movie__genre_set').filter(user_id=account_id)
            category_path = 'movie__genre__name'

        if category == 'country':
            stars = Star.objects.select_related('movie').filter(user_id=account_id)
            category_path = 'movie__country'

        context = {
            'wholeCount': len(stars),
            'watchingTime' : sum([star.movie.show_time for star in stars]),
            'data': [{
                        'label': star[category_path],
                        'score': int(star['avg']),
                        'count': star['count'],
                     } for star in stars.values(category_path).annotate(count=Count(category_path), avg=20 * Avg('point')).order_by('-avg')]
        }
        return JsonResponse(context, status=200)

class StarRatingView(View):
    @login_decorator
    def get(self, request):
        movie_id = request.GET.get('movie_id', None)
        if movie_id:
            moviequeryset  = Star.objects.filter(movie_id=movie_id)

            rating = {}
            for star in numpy.arange(0.5, 5.5, 0.5):
                rating[star] = moviequeryset.filter(point=star).count()
            return JsonResponse({'movie':rating}, status=200)

        else:
            user_id       = request.user.id
            userqueryset  = Star.objects.filter(user_id=user_id)

            rating = {}
            for star in numpy.arange(0.5, 5.5, 0.5):
                rating[star] = userqueryset.filter(point=star).count()
            return JsonResponse({'user':rating}, status=200)

class StarView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            star_check = Star.objects.filter(
                user_id  = request.user,
                movie_id = data["movieId"]
            )

            if star_check.exists():
                return JsonResponse({"message":"ALREADY_EXISTS"}, status=400)

            if float(data["starPoint"])*2 %1 != 0 or float(data["starPoint")] == 0:
                return JsonResponse({"message":"VALUE_ERROR"}, status=400)

            star = Star.objects.create(
                user_id  = request.user,
                movie_id = data["movieId"],
                point    = data["starPoint"]
            )

            feedback = {
                "starPoint"    : star.point
            }
            return JsonResponse(feedback, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class StarDetailView(View):
    @login_decorator
    def get(self, request, movie_id):
        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movie_id
        )

        if star.exists():
            star       = star.first()
            star_point = star.point
        else:
            return JsonResponse({"starPoint": 0}, status=404)

        feedback = {
            "starPoint" : star_point
        }
        return JsonResponse(feedback, status=200)

    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        try:
            star = Star.objects.filter(
                user_id  = request.user,
                movie_id = movie_id
            )

            if not star.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)

            if float(data["starPoint"])*2 %1 != 0 or float(data["starPoint"]) == 0:
                return JsonResponse({"message":"VALUE_ERROR"}, status=400)

            star        = star.first()
            star.point  = data["starPoint"]
            star.save()
            update_star = star.point
            feedback = {
                "starPoint"    : update_star
            }
            return JsonResponse(feedback, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, movie_id):

        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movie_id
        )

        if star.exists():
            star.delete()
        else:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        feedback = {
            "message": "SUCCESS"
        }
        return JsonResponse (feedback, status=204)
