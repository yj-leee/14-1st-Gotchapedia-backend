import json

from django.views    import View
from django.http     import JsonResponse #
from .models         import *

from user.models     import User
from anaylsis.models import *
from user.utils      import login_required

class CreateStarView(View):
    #<-- login decorator -->
    def post(self,reqest):
        data = json.loads(reqest.body)

        try:
            star = Star.objects.create(
                point    = data["starPoint"],
                user_id  = reqest.user,
                movie_id = data["movieId"]
            )

            feedback = [
                "message"   : "SUCCESS",
                "starPoint" : star.point
            )]
            return JsonResponse(feedback, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class ReadStarView(View):
    #<-- login decorator -->
    def get(self,reqest):
        data = json.loads(reqest.body)

        try:
            star     = star.objects.filter(
            movie_id = data["movieId"],
            user_id  = reqest.user
            )

            if star.exists():
                star       = star.first()
                star_point = star.point
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)

            feedback = [
                "message"   : "SUCCESS",
                "starPoint" : star_point
            )]
            return JsonResponse(feedback, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class UpdateStarView(View):
    #<-- login decorator -->
    def post(self,reqest):
        data = json.loads(reqest.body)

        try:
            star     = star.objects.filter(
            movie_id = data["movieId"]
            user_id  = request.user
            )

            if star.exists():
                star.update(point = date["starPoint"])
                update_star = star.point
            else:
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)

            feedback = [
                "message"   : "SUCCESS",
                "starPoint" : update_star
            )]
            return JsonResponse(feedback, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class DeleteStarView(View):
    #<-- login decorator -->
    def delete(self,reqest):
        data = json.loads(reqest.body)

        try:
            star = star.objects.filter(
            movie_id = data["movieId"]
            user_id  = request.user
            )

            if star.exists():
                star.delete()
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)

            feedback = [
                "message":"SUCCESS"
            ]
            return JsonResponse(feedback, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
