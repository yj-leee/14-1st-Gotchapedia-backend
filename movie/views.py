import json

from django.views import View
from django.http import JsonResponse

from .models import Movie
from analysis.models import Star

class UserFavoriteView(View):
    def get(self, request):
        account_id = request.GET.get('id')
        list_range = request.GET.get('range')

        if not account_id:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            stars = Star.objects.select_related('movie').filter(user_id=int(account_id)).order_by('-point').all()
            
            if list_range:
                range = min(stars.count(),int(list_range))
            else:
                range = stars.count()

            rank_data = {
                'data': [{
                    'movieId': star.movie.id,
                    'imageURL': star.movie.main_image,
                    'title': star.movie.name,
                    'rate': star.point,
                    'date': f'{star.movie.opening_at.year} . {star.movie.country}'
                 } for star in stars[:range]]
            }
            return JsonResponse(rank_data, status=200)
        except ValueError:
            return JsonResponse({'message': 'INSTANCE_IS_NOT_NUMBER'}, status=400)