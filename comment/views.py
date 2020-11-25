import json

from django.views    import View
from django.http     import JsonResponse
from django.db.models import Count

from .models         import Comment
from users.utils     import login_decorator

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
    def get(self, request, reply_id):
        pass

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
