import json

from django.views import View
from django.http import JsonResponse

from .models import Movie
from users.models import User

class UserFavoriteView(View):
    def post(self, request):
        #유저가 좋아하는(별점) TOP 10의 영화 정보
        NECESSERY_KEYS = ('name',)
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data,NECESSERY_KEYS)):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            user   = User.objects.get(name=data['name'])
            stars  = user.star_set.order_by('-point').all()[:10]
            movies = [star.movie for star in stars]
            content = {
                'message': 'SUCCESS',
                'data': [{
                            'movieimg': movie.main_image,
                            'movietitle': movie.name,
                            'movierate': f'{stars[i].point}',
                            'rank': i+1,
                            'moviedate': f'{movie.opening_at.year} . {movie.country}'
                        } for i, movie in enumerate(movies)]
            }
            return JsonResponse(content, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'NOT_EXIST_USER'}, status=400)
