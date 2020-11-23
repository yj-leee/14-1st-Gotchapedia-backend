import json
import requests

from django.views import View
from django.http import JsonResponse
from .models import Movie
from .models import Staff
from users.models import User



class SearchView(View):
    def get(self, request):
        search_key = request.GET.get('searchkey',None)
        if Movie.objects.filter(name__icontains=search_key).exists():
            moviequeryset = Movie.objects.filter(name__icontains=search_key)
            movielist = []
            for movie in moviequeryset:
               movielist.append({
                    'name'     : movie.name,
                    'image'    : movie.main_image,
                    'country'  : movie.country,
                    'year'     : movie.opening_at
               })
            return JsonResponse({'result': movielist}, status=200)

        elif Staff.objects.filter(name__icontains=search_key).exists():
            moviequeryset = Staff.objects.filter(name__icontains=search_key)
            movielist = []
            for moviequery in moviequeryset:
                for movie in moviequery.movie.all():
                    movielist.append({
                        'name'     : movie.name,
                        'country'  : movie.country,
                        'year'     : movie.opening_at
                    })
            return JsonResponse({'result' : movielist}, status=200)
        else:
            return JsonResponse({'result' : None}, status=400)
