import json

from django.views    import View
from django.http     import JsonResponse

from .models         import Comment, Like
from movie.models    import Movie
from users.models    import User
from users.utils     import login_decorator

class CommentLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            target = Comment.objects.filter(id=data["commentId"])
            like_check = Like.objects.filter(
                user_id    = request.user,
                comment_id = data["commentId"]
            )

            if not target.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)
            if like_check.exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=404)
            else:
                like = Like.objects.create(
                    user_id    = request.user,
                    comment_id = data["commentId"]
            )

            feedback = {
                "message": "SUCCESS"
            }
            return JsonResponse(feedback, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, comment_id):
        comment = Comment.objects.filter(id = comment_id)

        if comment.exists():
            comment.delete()
        else:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        feedback = {
            "message": "SUCCESS"
        }
        return JsonResponse (feedback, status=204)
