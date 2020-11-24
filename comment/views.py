import json

from django.views    import View
from django.http     import JsonResponse
from django.db.models import Count

from .models         import Comment, Like
from movie.models    import Movie
from users.models    import User
from analysis.models import Star, Interest
from users.utils     import login_decorator


class CommentListView(View):
    @login_decorator
    def get(self, request, movie_id):

        comments = Comment.objects.select_related('user').prefetch_related('user__star_set',
                                                                           'like_set',
                                                                           'main_comment').filter(movie_id=movie_id)

        comment_list = [{
            "id": comment.id,
            "userName": comment.user.name,
            "userImage": comment.user.profile_image,
            "starPoint" : comment.user.star_set.get(movie_id=movie_id).point,
            "content": comment.content,
            "likeCount": comment.like_set.count(),
            "replyCount": comment.main_comment.count()-1,
        } for comment in comments if comment.id == comment.comment_id]

        return JsonResponse({"data":comment_list}, status=200)
