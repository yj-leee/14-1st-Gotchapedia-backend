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
    """
    특정 영화에 대한 별점 평가 생성

    Author: 고수희

    History: 2020-11-19(고수희) : 초기 생성
             2020-11-20(고수희) : 1차 수정 - 로직 수정
             2020-11-21(고수희) : 2차 수정 - 데코레이터 적용
             2020-11-23(고수희) : 3차 수정 - view 분리
             2021-01-20(고수희) : 4차 수정 - 변수 명 수정, 주석 추가

    Returns: 생성된 별점 점수

    """

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            star_check = Star.objects.filter(
                user_id  = request.user,
                movie_id = data["movieId"]
            )

            # 평가한 별점이 이미 있는 경우
            if star_check.exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=400)

            # 평가 별점이 0.5 단위가 아닐 경우
            if float(data["starPoint"])*2%1 != 0 or float(data["starPoint"] == 0):
                return JsonResponse({"message": "VALUE_ERROR"}, status=400)

            star = Star.objects.create(
                user_id  = request.user,
                movie_id = data["movieId"],
                point    = data["starPoint"]
            )

            return JsonResponse({"starPoint": star.point}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class StarDetailView(View):
    """
    영화 별점 정보 조회

    Author: 고수희

    History: 2020-11-19(고수희) : 초기 생성
             2020-11-20(고수희) : 1차 수정 - 로직 수정
             2020-11-21(고수희) : 2차 수정 - 데코레이터 적용
             2020-11-23(고수희) : 3차 수정 - view 분리
             2021-01-20(고수희) : 4차 수정 - 변수 명 수정, 주석 추가

    Returns: 유저가 평가한 별점 정보

    """

    @login_decorator
    def get(self, request, movie_id):
        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movie_id
        )

        if star.exists():
            star       = star.first()
            star_point = star.point

        # 평가한 별점이 없는 경우 0 점으로 반환
        else:
            return JsonResponse({"starPoint": 0}, status=404)

        return JsonResponse({"starPoint": star_point}, status=200)

    """
    영화 별점 정보 수정

    Author: 고수희

    History: 2020-11-19(고수희) : 초기 생성
             2020-11-20(고수희) : 1차 수정 - 로직 수정
             2020-11-21(고수희) : 2차 수정 - 데코레이터 적용
             2020-11-23(고수희) : 3차 수정 - view 분리
             2021-01-20(고수희) : 4차 수정 - 변수 명 수정, 주석 추가

    Returns: 유저가 수정 평가한 별점 정보

    """

    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        try:
            star = Star.objects.filter(
                user_id  = request.user,
                movie_id = movie_id
            )

            # 수정할 별점이 없을 경우
            if not star.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)

            # 평가 별점이 0.5 단위가 아닐 경우
            if float(data["starPoint"])*2%1 != 0 or float(data["starPoint"] == 0):
                return JsonResponse({"message": "VALUE_ERROR"}, status=400)

            star        = star.first()
            star.point  = data["starPoint"]
            star.save()
            update_star = star.point

            return JsonResponse({"starPoint": update_star}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    """
    영화 별점 정보 삭

    Author: 고수희

    History: 2020-11-19(고수희) : 초기 생성
             2020-11-20(고수희) : 1차 수정 - 로직 수정
             2020-11-21(고수희) : 2차 수정 - 데코레이터 적용
             2020-11-23(고수희) : 3차 수정 - view 분리
             2021-01-20(고수희) : 4차 수정 - 변수 명 수정, 주석 추가

    Returns: SUCCESS

    """

    @login_decorator
    def delete(self, request, movie_id):

        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movie_id
        )

        # 삭제할 별점이 없을 경우
        if not star.exists():
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        star.delete()

        return JsonResponse({"message": "SUCCESS"}, status=204)
