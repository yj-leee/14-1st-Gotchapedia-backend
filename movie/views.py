import json

from django.views import View
from django.http import JsonResponse

from .models import (
    Movie,
    Picture,
    Actor,
    MovieActor,
    Genre,
    MovieGenre
)

from users.models import User
from analysis.models import Star


class CreateStarView(View):
#    <-- login decorator -->
    def post(self, request):
        data = json.loads(request.body)

        try:
            star = Star.objects.create(
                user_id = request.user,
                movie_id = data["movieId"],
                point = data["starPoint"]
            )

            feedback = [
                {"message":"SUCCESS"},
                {"starPoint":star.point}
            ]
            return JsonResponse(feedback, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class ReadStarView(View):
#    <-- login decorator -->
    def get(self, request):
        data = request.GET.get('movieId')

        star = Star.objects.filter(
            user_id = request.user,
            movie_id = data["movieId"]
        )

        if star.exists():
            star = star.first()
            star_point = star.point
        else:
            return JsonResponse({"message":"NOT_FOUND"}, status =404)

        feedback = [
            {"message":"SUCCESS"},
            {"starPoint":star_point}
        ]
        return JsonResponse(feedback, status = 200)


class UpdateStarView(View):
#    <-- login decorator -->
    def post(self, request):
        data = json.loads(request.body)

        try:
            star = star.objects.filter(
                user_id = request.user,
                movie_id = data["movieId"]
            )

            if star.exists():
                star.update(point = data["starPoint"])
                update_star = star.point
            else:
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)

            feedback = [
                {"message":"SUCCESS"},
                {"starPoint":update_star}
            ]
            return JsonResponse(feedback, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class DeleteStarView(View):
#    <-- login decorator -->
    def delete(self, request):
        data = request.GET.get(movieId)

        star = star.objects.filter(
            user_id = request.user,
            movie_id = data["movieId"]
        )

        if star.exists():
            star.delete()
        else:
            return JsonResponse({"message":"NOT_FOUND"}, status = 404)

        feedback = [
            {"message":"SUCCESS"}
        ]
        return JsonResponse (feedback, status = 200)
