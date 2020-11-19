import json

from django.views import View
from django.http import JsonResponse

from .models import Movie
from analysis.models import Star

class UserFavoriteView(View):
    def get(self, request):
        account_id = request.GET.get('id')
        list_range = request.GET.get('range')

        if not account_id or not list_range:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            stars  = Star.objects.filter(user_id=int(account_id)).order_by('-point')[:int(list_range)]
            movies = [star.movie for star in stars]

            content = {
                'message': 'SUCCESS',
                'data': [{
                            'imageURL': movie.main_image,
                            'title': movie.name,
                            'rate': f'{stars[i].point}',
                            'rank': i+1,
                            'date': f'{movie.opening_at.year} . {movie.country}'
                        } for i, movie in enumerate(movies)]
            }
            return JsonResponse(content, status=200)
        except ValueError:
            return JsonResponse({'message': 'INSTANCE_IS_NOT_NUMBER'}, status=400)
