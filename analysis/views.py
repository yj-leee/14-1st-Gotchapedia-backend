import json

from django.views import View
from django.http import JsonResponse
from django.db.models import  Count, Avg

from movie.models import Movie
from analysis.models import Star
from users.utils import login_decorator

class FavoriteView(View):
    @login_decorator
    def get(self, request):
        account_id = request.user
        category   = request.GET.get('category', 'genre') # '장르(genre)' 또는 '국가(country)'

        stars = []
        category_path = ''

        if category == 'genre':
            stars = Star.objects.select_related('movie').prefetch_related('movie__genre_set').filter(user_id=account_id)
            category_path = 'movie__genre__name'

        if category == 'country':
            stars = Star.objects.select_related('movie').filter(user_id=account_id)
            category_path = 'movie__country'

        context = {
            'wholeCount': len(stars),
            'watchingTime' : sum([star.movie.show_time for star in stars]),
            'data': [{
                        'label': star[category_path],
                        'score': int(star['avg']),
                        'count': star['count'],
                     } for star in stars.values(category_path).annotate(count=Count(category_path), avg=20 * Avg('point')).order_by('-avg')]
        }
        return JsonResponse(context, status=200)
