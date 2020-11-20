import json

from django.views import View
from django.http import JsonResponse

from .models import Movie
from analysis.models import Star

class UserFavoriteView(View):
    def get(self, request):
        account_id = request.GET.get('id')
        list_range = request.GET.get('range', 10)

        if not account_id:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            rank_data = {
                'data': [{
                            'imageURL': star.movie.main_image,
                            'title': star.movie.name,
                            'rate': star.point,
                            'date': f'{star.movie.opening_at.year} . {star.movie.country}'
                 } for star in Star.objects.filter(user_id=int(account_id)).order_by('-point')[:int(list_range)]]
            }#select related 써서 데이터 베이스 호출 줄일 것!!!!! 
            return JsonResponse(rank_data, status=200)
        except ValueError:
            return JsonResponse({'message': 'INSTANCE_IS_NOT_NUMBER'}, status=400)
