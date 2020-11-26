import json
import requests
from operator         import itemgetter

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count

from .models          import Movie, MovieStaffPosition, Comment, Like
from analysis.models  import Star, Interest
from users.utils      import login_decorator


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
                    'movieId'  : star.movie.id,
                    'imageURL' : star.movie.main_image,
                    'title'    : star.movie.name,
                    'rate'     : star.point,
                    'date'     : f'{star.movie.opening_at.year} . {star.movie.country}'
                 } for star in stars]
            }
            return JsonResponse(context, status=200)
        except ValueError:
            return JsonResponse({'message': 'INSTANCE_IS_NOT_NUMBER'}, status=400)


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
                'movieId'  : interest.movie.id,
                'imageURL' : interest.movie.main_image,
                'title'    : interest.movie.name,
                'rate'     : str(round(sum([star.point for star in interest.movie.star_set.all()])/max(interest.movie.star_set.all().count(),1))),
                'date'     : f'{interest.movie.opening_at.year} . {interest.movie.country}'
                } for interest in interests]
        }
        return JsonResponse(data, status=200)


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
            'id'     : interest.id,
            'status' : interest.status
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
                'id'     : interest.id,
                'status' : interest.status
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
            "replyList"  : [{"replyId"        : reply.id,
                             "replyUserName"  : reply.user.name,
                             "replyUserImage" : reply.user.profile_image,
                             "replyContent"   : reply.content,
                             "replyLikeCount" : reply.like_set.count()
                            } for reply in comment.main_comment.all() if reply.id != reply.comment_id]
        } for comment in comments if comment.id == comment.comment_id]

        ordered_list = sorted(comment_list, key=itemgetter("likeCount"), reverse=True)

        return JsonResponse({"data": ordered_list}, status=200)


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
                "id"      : comment.id,
                "content" : comment.content
            }
            return JsonResponse({"message": feedback}, status=200)

        except KeyError:
            return Jsonresponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def get(self, request, comment_id):
        check_comment = Comment.objects.filter(id=comment_id)

        if not check_comment.exists():
            return JsonResponse({"message": "NO_COMMENT"}, status=400)

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
    def patch(self, request, comment_id):
        data = json.loads(request.body)

        try:
            check_comment = Comment.objects.filter(id=comment_id)

            if not check_comment.exists():
                return JsonResponse({"message": "NO_COMMENT"}, status=400)

            comment         = check_comment.first()
            comment.content = data["content"]
            comment.save()
            update_comment  = comment.content

            feedback = {
                "content"    : update_comment
            }
            return JsonResponse(feedback, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, comment_id):
        check_comment = Comment.objects.filter(id=comment_id)

        if not check_comment.exists():
            return JsonResponse({"message": "NO_COMMENT"}, status=404)

        check_comment.delete()

        feedback = {
            "message": "SUCCESS"
        }
        return JsonResponse(feedback, status=204)


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


class ReplyView(View):
    @login_decorator
    def post(self, request, comment_id):
        data = json.loads(request.body)

        if 'content' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'message': 'NO_COMMENT'}, status=400)

        reply = Comment.objects.create(user_id=request.user.id,comment_id=comment_id, content=data['content'])

        context = {
            'id'      : reply.id,
            'content' : reply.content
        }
        return JsonResponse(context, status=201)

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
            "id"        : reply.id,
            "userName"  : request.user.name,
            "userImage" : request.user.profile_image,
            "content"   : reply.content,
            "likeCount" : reply.like_set.count(),
        }
        return JsonResponse(context, status=200)

    @login_decorator
    def delete(self, request, reply_id):
        if not Comment.objects.filter(id = reply_id).exists():
            return JsonResponse({'message': 'NO_REPLY'}, status=400)

        reply = Comment.objects.filter(id=reply_id)
        reply.delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)
