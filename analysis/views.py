import json

from django.views import View
from django.http  import JsonResponse

from .models      import Star
from users.models import User
from movie.models import Movie
from users.utils  import login_decorator


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

            if data["starPoint"]*2 %1 != 0 or data["starPoint"] == 0:
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

            if data["starPoint"]*2 %1 != 0 or data["starPoint"] == 0:
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
