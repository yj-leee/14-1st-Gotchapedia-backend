import json

from django.views import View
from django.http import JsonResponse

from movie.models import Movie
from analysis.models import Star
from users.utils import login_decorator

class FavoriteView(View):
    @login_decorator
    def get(self, request):
        account_id = request.user
        category   = request.GET.get('category', 'genre') # '장르(genre)' 또는 '국가(country)'

        results = {}
        stars = []

        if category == 'genre':
            stars = Star.objects.select_related('movie').prefetch_related('movie__genre_set').filter(user_id=account_id)
            for star in stars:
                for genre in star.movie.genre_set.all():
                    if not genre.name in results:
                        results[genre.name] = {'count': 0, 'score': 0}
                    results[genre.name]['count'] += 1
                    results[genre.name]['score'] += star.point

        if category == 'country':
            stars = Star.objects.select_related('movie').filter(user_id=account_id)
            for star in stars:
                if not star.movie.country in results:
                    results[star.movie.country] = {'count': 0, 'score': 0}
                results[star.movie.country]['count'] += 1
                results[star.movie.country]['score'] += star.point

        for result in results.values():
            result['score'] = int(result['score'] / result['count'] * 20)

        content = {
            'wholeCount': len(stars),
            'watchingTime' : sum([star.movie.show_time for star in stars]),
            'data': sorted([{
                        'label': key,
                        'score': value['score'],
                        'count': value['count'],
            } for key, value in results.items()], key=lambda data: data['score'], reverse=True)
        }
        return JsonResponse(content, status=200)
