import json
from operator         import itemgetter

from django.views    import View
from django.http     import JsonResponse
from django.db.models import Count

from .models          import Comment, Like
from movie.models     import Movie
from users.models     import User
from analysis.models  import Star
from users.utils      import login_decorator

class CommentView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
       
        try:
            movie_check = Movie.objects.filter(id = data["movieId"])
            star_check  = Star.objects.filter(
                user_id  = request.user.id,
                movie_id = data["movieId"]
            )

            if not movie_check.exists():
                return JsonResponse({"message": "NO_MOVIE"}, status=400)

            if not star_check.exists():
                return JsonResponse({"message":" NO_PERMISSION"}, status=403)

            comment_check = Comment.objects.filter(
                user_id  = request.user.id,
                movie_id = data["movieId"]
            )

            if comment_check.exists():
                return JsonResponse({"message": "ALREADY_EXIST"}, status=400)

            comment = Comment.objects.create(
                user_id    = request.user.id,
                movie_id   = data["movieId"],
                content    = data["content"]
            )

            comment.comment_id = comment.id
            comment.save()

            feedback = {
                "content" : comment.content
            }
            return jsonresponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def get(self, request, movie_id):
        movie_check = Movie.objects.filter(id=movie_id)

        if not movie_check.exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        check_comment = Comment.objects.filter(
            user_id  = request.user.id,
            movie_id = movie_id
        )

        comment  = ''
        if check_comment.exists():
            comment = check_comment.first()
            comment = comment.content
        else:
            comment = ''

        feedback = {
            "content" : comment
        }
        return JsonResponse(feedback, status=200)

    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        try:
            movie_check = Movie.objects.filter(id=movie_id)

            if not movie_check.exists():
                return JsonResponse({"message": "NO_MOVIE"}, status=400)

            comment = Comment.objects.filter(
                user_id  = request.user.id,
                movie_id = movie_id
            )

            if comment.exists():
                comment         = comment.first()
                comment.content = data["content"]
                comment.save()
                update_comment  = comment.content
            else:
                return JsonResponse({"message": "NOT_FOUND"}, status=404)

            feedback = {
                "content"    : update_comment
            }
            return JsonResponse(feedback, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, movie_id):
        movie_check = Movie.objects.filter(id=movie_id)

        comment = Comment.objects.filter(
            user_id  = request.user.id,
            movie_id = movie_id
        )

        if not movie_check.exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        if not comment.exists():
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        comment.delete()

        feedback = {
            "message": "SUCCESS"
        }
        
        return JsonResponse(feedback, status=204)
      
  
class CommentListView(View):
    @login_decorator
    def get(self, request, movie_id):

        comments = Comment.objects.select_related(
            'user').prefetch_related('user__star_set',
                                     'like_set',
                                     'main_comment').filter(movie_id=movie_id)

        comment_list = [{
            "id"         : comment.id,
            "userName"   : comment.user.name,
            "userImage"  : comment.user.profile_image,
            "starPoint"  : comment.user.star_set.get(movie_id=movie_id).point,
            "content"    : comment.content,
            "likeCount"  : comment.like_set.count(),
            "replyCount" : comment.main_comment.count()-1,
        } for comment in comments if comment.id == comment.comment_id]

        ordered_list = sorted(comment_list, key=itemgetter("likeCount"), reverse=True)

        return JsonResponse({"data": ordered_list}, status=200)

      
class CommentLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            comment = Comment.objects.filter(id=data["commentId"])
            like_check = Like.objects.filter(
                user_id    = request.user.id,
                comment_id = data["commentId"]
            )

            if not comment.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)
            if like_check.exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=404)
            else:
                like = Like.objects.create(
                    user_id    = request.user.id,
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
        like = Like.objects.filter(
            user_id    = request.user.id,
            comment_id = comment_id
        )

        if not like.exists():
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

        like.delete()
        feedback = {
            "message": "SUCCESS"
        }
        return JsonResponse (feedback, status=204)
 
class ReplyListView(View):
    @login_decorator
    def get(self, request, comment_id):

        comments = Comment.objects.select_related('user').prefetch_related('like_set').filter(comment_id=comment_id)

        comment_list = [{
            "id": comment.id,
            "userName": comment.user.name,
            "userImage": comment.user.profile_image,
            "content": comment.content,
            "likeCount": comment.like_set.count(),
        } for comment in comments]

        return JsonResponse({"data":comment_list}, status=200)

    @login_decorator
    def post(self, request, comment_id):
        data = json.loads(request.body)

        if 'content' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'message': 'NO_COMMENT'}, status=400)

        reply = Comment.objects.create(user_id=request.user.id, comment_id=comment_id, content=data['content'])

        context = {
            'id': reply.id,
            'content': reply.content
        }
        return JsonResponse(context, status=201)

class ReplyView(View):
    @login_decorator
    def patch(self, request, reply_id):
        data = json.loads(request.body)

        if 'content' not in data.keys():
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if not Comment.objects.filter(id = reply_id).exists():
            return JsonResponse({'message': 'NO_REPLY'}, status=400)

        reply = Comment.objects.prefetch_related('like_set').get(id=reply_id)
        reply.content = data['content']
        reply.save()

        context = {
            "id": reply.id,
            "userName": request.user.name,
            "userImage": request.user.profile_image,
            "content": reply.content,
            "likeCount": reply.like_set.count(),
        }
        return JsonResponse(context, status=200)

    @login_decorator
    def delete(self, request, reply_id):
        if not Comment.objects.filter(id = reply_id).exists():
            return JsonResponse({'message': 'NO_REPLY'}, status=400)

        reply = Comment.objects.filter(id=reply_id)
        reply.delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)
