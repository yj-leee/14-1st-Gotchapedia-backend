import json

from django.views import View
from django.http  import JsonResponse

from .models      import Star
from users.models import User
from movie.models import Movie


class StarView(View):
#    <-- login decorator -->
    def post(self, request, movieId):
        data = json.loads(request.body)

        try:
            star_check = Star.objects.filter(
                user_id = request.user,
                movie_id = movieId
            )

            if star_check.exists():
                return JsonResponse({"message":"ALREADY_EXISTS"}, status=400)

            star = Star.objects.create(
                user_id  = request.user,
                movie_id = movieId,
                point    = data["starPoint"]
            )

            feedback = {
                "starPoint"    : star.point
            }
            return JsonResponse(feedback, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request, movieId):

        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movieId
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

#    <-- login decorator -->
    def patch(self, request, movieId):
        data = json.loads(request.body)

        try:
            star = Star.objects.filter(
                user_id  = request.user,
                movie_id = movieId
            )

            if not star.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)

            star = star.first()
            if not star.point >= 0.5:
                return JsonResponse({"message":"METHOD_ALLOWED"}, status=400)

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

#    <-- login decorator -->
    def delete(self, request, movieId):

        star = Star.objects.filter(
            user_id  = request.user,
            movie_id = movieId
        )

        if star.exists():
            star.delete()
        else:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        feedback = {
            "message": "SUCCESS"
        }
        return JsonResponse (feedback, status=204)
