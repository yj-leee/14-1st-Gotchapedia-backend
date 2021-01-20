import json
import requests
from operator import itemgetter

from django.views import View
from django.http import JsonResponse
from django.db.models import Count, Q

from .models import Movie, MovieStaffPosition, Comment, Like
from analysis.models import Star, Interest
from users.utils import login_decorator


class SearchView(View):
    def get(self, request):
        search_key = request.GET.get('searchkey', None)
        queryset = MovieStaffPosition.objects.filter(
            Q(staff__name__icontains=search_key) | Q(movie__name__icontains=search_key))

        movielist = [{
            'name': movie.movie.name,
            'image': movie.movie.main_image,
            'country': movie.movie.country,
            'year': movie.movie.opening_at
        } for movie in queryset]

        return JsonResponse({'result': movielist}, status=200)


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
                    'movieId': star.movie.id,
                    'imageURL': star.movie.main_image,
                    'title': star.movie.name,
                    'rate': star.point,
                    'date': f'{star.movie.opening_at.year} . {star.movie.country}'
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

        interests = Interest.objects.select_related('movie').prefetch_related('movie__star_set').filter(
            user_id=account_id)

        if status:
            interests = interests.filter(status=status)

        data = {
            'data': [{
                'movieId': interest.movie.id,
                'imageURL': interest.movie.main_image,
                'title': interest.movie.name,
                'rate': str(round(sum([star.point for star in interest.movie.star_set.all()]) / max(
                    interest.movie.star_set.all().count(), 1))),
                'date': f'{interest.movie.opening_at.year} . {interest.movie.country}'
            } for interest in interests]
        }
        return JsonResponse(data, status=200)


class MovieInfoView(View):
    """
    영화 상세 정보 조회

    Author: 고수희

    History: 2020-11-21(고수희) : 초기 생성
             2020-11-24(고수희) : 1차 수정 - prefetch_related, select_related 를 사용
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Return: 영화 상세 정보

    """

    @login_decorator
    def get(self, request, movie_id):

        try:
            movie_info = Movie.objects.prefetch_related('moviegenre_set',
                                                        'picture_set',
                                                        'moviestaffposition_set').get(id=movie_id)

            movie_infos = {
                "id": movie_info.pk,  # 영화 id
                "name": movie_info.name,  # 영화 이름
                "country": movie_info.country,   # 영화 개봉 국가
                "description": movie_info.description,  # 영화 설명
                "mainImage": movie_info.main_image,  # 영화 포스터
                "openDate": movie_info.opening_at.year,  # 영화 개봉일
                "showTime": movie_info.show_time,  # 영화 러닝타임
                "genre": [{"name": genre.genre.name
                           } for genre in movie_info.moviegenre_set.select_related('genre')],
                "staff": [{"name": staff.staff.name,
                           "image": staff.staff.proflie_image,
                           "position": staff.position.name
                           } for staff in movie_info.moviestaffposition_set.select_related('staff', 'position')],  # 배우 및 감독
                "subImage": [{"url": image.url
                              } for image in movie_info.picture_set.all()]  # 영화 갤러리 이미
            }
            return JsonResponse({"data": movie_infos}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class MovieDetailView(View):
    """
    영화 상세 정보 더보기 조회

    Author: 고수희

    History: 2020-11-21(고수희) : 초기 생성
             2020-11-24(고수희) : 1차 수정 - prefetch_related, select_related 를 사용
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: 영화 상세 더보기 정보

    """

    @login_decorator
    def get(self, request, movie_id):

        try:
            movie_info = Movie.objects.prefetch_related('moviegenre_set').get(id=movie_id)

            movie_infos = {
                "id": movie_info.id,  # 영화 id
                "name": movie_info.name,  # 영화 이름
                "country": movie_info.country,  # 영화 개봉 국가
                "description": movie_info.description,  # 영화 설명
                "openDate": movie_info.opening_at.year,  # 영화 개봉일
                "showTime": movie_info.show_time,  # 영화 러닝타임
                "genre": [{"name": genre.genre.name
                           } for genre in movie_info.moviegenre_set.select_related('genre')]  # 영화 장르
            }
            return JsonResponse({"data": movie_infos}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class InterestView(View):
    @login_decorator
    def post(self, request, movie_id):
        data = json.loads(request.body)

        if 'status' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if not Movie.objects.filter(id=movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            return JsonResponse({"message": "ALREADY_EXIST"}, status=400)

        interest = Interest.objects.create(user_id=request.user, movie_id=movie_id, status=data["status"])

        context = {
            'id': interest.id,
            'status': interest.status
        }
        return JsonResponse(context, status=201)

    @login_decorator
    def get(self, request, movie_id):

        if not Movie.objects.filter(id=movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        context = {}
        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            interest = Interest.objects.get(user_id=request.user, movie_id=movie_id)
            context = {
                'id': interest.id,
                'status': interest.status
            }
        return JsonResponse(context, status=200)

    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        if 'status' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if not Movie.objects.filter(id=movie_id).exists():
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

        if not Movie.objects.filter(id=movie_id).exists():
            return JsonResponse({'message': 'NO_MOVIE'}, status=400)

        interest = Interest.objects.filter(user_id=request.user, movie_id=movie_id)
        interest.delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)


class CommentListView(View):
    """
    특정 영화에 생성된 댓글 리스트 조회

    Author: 고수희

    History: 2020-11-24(고수희) : 초기 생성
             2020-11-27(고수희) : 1차 수정 - 리스트 조회 시 대댓글 리스트도 함께 나오도록 수정
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: 댓글 정보 리스트

    """

    @login_decorator
    def get(self, request, movie_id):
        comments = Comment.objects.select_related(
            'user').prefetch_related('user__star_set',
                                     'like_set',
                                     'main_comment').filter(movie_id=movie_id)

        comment_list = [{
            "id": comment.id,  # 댓글 id
            "userName": comment.user.name,  # 댓글 작성 유저 닉네임
            "userImage": comment.user.profile_image,  # 댓글 작성 유저 이미지
            "starPoint": comment.user.star_set.get(movie_id=movie_id).point,  # 댓글 작성자가 해당 영화에 남긴 별점
            "content": comment.content,  # 댓글 내용
            "likeCount": comment.like_set.count(),  # 해당 댓글에 달린 좋아요 갯수
            "replyCount": comment.main_comment.count() - 1,  # 해당 댓글에 달린 대댓글 갯수
            "replyList": [{"replyId": reply.id,  # 대댓글 id
                           "replyUserName": reply.user.name,  # 대댓글 작성 유저 닉네임
                           "replyUserImage": reply.user.profile_image,  # 대댓글 작성 유저 이미지
                           "replyContent": reply.content,  # 대댓글 내용
                           "replyLikeCount": reply.like_set.count()  # 해당 대댓글에 달린 좋아요 갯수
                           } for reply in comment.main_comment.all() if reply.id != reply.comment_id]
        } for comment in comments if comment.id == comment.comment_id]

        ordered_list = sorted(comment_list, key=itemgetter("likeCount"), reverse=True)  # 좋아요 갯수만큼 댓글 리스트 정렬

        return JsonResponse({"data": ordered_list}, status=200)


class CommentView(View):
    """
    특정 영화에 대한 댓글 생성

    Author: 고수희

    History: 2020-11-24(고수희) : 초기 생성
             2020-11-27(고수희) : 1차 수정 - 데코레이터 수정
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: 생성된 댓글 id와 댓글 내용

    Note:
        댓글은 영화에 별점을 남긴 사람만 남길 수 있음

    """

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            movie_check = Movie.objects.filter(id=data["movieId"])
            star_check = Star.objects.filter(
                user_id=request.user.id,
                movie_id=data["movieId"]
            )

            # 영화가 없을 경우
            if not movie_check.exists():
                return JsonResponse({"message": "NO_MOVIE"}, status=400)

            # 유저가 별점을 남기지 않았을 경우
            if not star_check.exists():
                return JsonResponse({"message": " NO_PERMISSION"}, status=403)

            comment_check = Comment.objects.filter(
                user_id=request.user.id,
                movie_id=data["movieId"]
            )

            # 이미 작성된 코멘트가 있는 경우
            if comment_check.exists():
                return JsonResponse({"message": "ALREADY_EXIST"}, status=400)

            comment = Comment.objects.create(
                user_id=request.user.id,
                movie_id=data["movieId"],
                content=data["content"]
            )

            result = {
                "id": comment.id,
                "content": comment.content
            }
            return JsonResponse({"message": result}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    """
    특정 영화에 대한 유저가 남긴 댓글 조회
    Author: 고수희

    History: 2020-11-24(고수희) : 초기 생성
             2020-11-27(고수희) : 1차 수정 - 데코레이터 수정
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: 생성된 댓글 id와 댓글 내용

    Note:
        댓글이 없어도 에러처리 하지 않음

    """
    @login_decorator
    def get(self, request, comment_id):
        check_comment = Comment.objects.filter(id=comment_id)

        if not check_comment.exists():
            return JsonResponse({"message": "NO_COMMENT"}, status=400)

        # 만약 댓글이 있을 경우 댓글 내용 반환, 댓글이 없을 경우 빈 문자열로 반환
        comment = ''
        if check_comment.exists():
            comment = check_comment.first()
            comment = comment.content
        else:
            comment = ''

        feedback = {
            "content": comment
        }
        return JsonResponse(feedback, status=200)

    """
    특정 영화에 대한 댓글 내용 수정

    Author: 고수희

    History: 2020-11-24(고수희) : 초기 생성
             2020-11-27(고수희) : 1차 수정 - 데코레이터 수정
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: 수정된 댓글 내용

    """

    @login_decorator
    def patch(self, request, comment_id):
        data = json.loads(request.body)

        try:
            check_comment = Comment.objects.filter(id=comment_id)

            # 댓글이 없는 경우
            if not check_comment.exists():
                return JsonResponse({"message": "NO_COMMENT"}, status=400)

            comment = check_comment.first()
            comment.content = data["content"]
            comment.save()

            update_comment = {
                "content": comment.content
            }
            return JsonResponse(update_comment, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    """
    댓글 삭제

    Author: 고수희

    History: 2020-11-24(고수희) : 초기 생성
             2020-11-27(고수희) : 1차 수정 - 데코레이터 수정
             2021-01-20(고수희) : 2차 수정 - 변수 명 수정, 주석 추가

    Returns: SUCCESS

    """

    @login_decorator
    def delete(self, request, comment_id):
        check_comment = Comment.objects.filter(id=comment_id)

        # 삭제할 댓글이 없는 경우
        if not check_comment.exists():
            return JsonResponse({"message": "NO_COMMENT"}, status=404)

        check_comment.delete()
        return JsonResponse({"message": "SUCCESS"}, status=204)


class CommentLikeView(View):
    """
    댓글 좋아요 생성/삭제

    Author: 고수희

    History: 2020-11-23(고수희) : 초기 생성
             2020-11-23(고수희) : 1차 수정 - 데코레이터 수정
             2021-01-20(고수희) : 2차 수정 - 로직 수정(POST 에서 좋아요 생성/삭제), 주석 추가

    Return:
        좋아요 생성할 경우 : SUCCESS
        좋아요 삭제할 경우 : DELETE_SUCCESS

    """

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            comment = Comment.objects.filter(id=data["commentId"])
            like = Like.objects.filter(
                user_id=request.user.id,
                comment_id=data["commentId"]
            )

            # 좋아요할 코멘트가 없을 경우
            if not comment.exists():
                return JsonResponse({"message": "NOT_FOUND"}, status=404)

            # 이미 좋아요를 한 경우 좋아요 삭제 처리
            if like.exists():
                like.delete()
                return JsonResponse({"message": "DELETE_SUCCESS"}, status=204)

            else:
                Like.objects.create(
                    user_id=request.user.id,
                    comment_id=data["commentId"]
                )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class ReplyView(View):
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

    @login_decorator
    def patch(self, request, reply_id):
        data = json.loads(request.body)

        if 'content' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if not Comment.objects.filter(id=reply_id).exists():
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
        if not Comment.objects.filter(id=reply_id).exists():
            return JsonResponse({'message': 'NO_REPLY'}, status=400)

        reply = Comment.objects.filter(id=reply_id)
        reply.delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)
