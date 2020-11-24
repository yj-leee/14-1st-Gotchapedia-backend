import json

from django.views import View
from django.http import JsonResponse

from .models import Movie
from analysis.models import Star, Interest
from users.utils import login_decorator

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
            'id': interest.id,
            'status': interest.status
        }
        return JsonResponse(context, status=201)
    
    @login_decorator
    def get(self, request, movie_id):

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        context = {}
        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            context = {
                'id': interest.id,
                'status': interest.status
            }
        return JsonResponse(context, status=200)
    
    @login_decorator
    def patch(self, request, movie_id):
        data = json.loads(request.body)

        if 'status' not in data.keys():
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        if not Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            return JsonResponse({"message": "NO_INTEREST"}, status=400)

        interest = Interest.objects.update(user_id=request.user, movie_id=movie_id, status=data["status"])

        context = {
            'id': interest.id,
            'status': interest.status
        }
        return JsonResponse(context, status=200)

    @login_decorator
    def delete(self, request, movie_id):

        if not Movie.objects.filter(id = movie_id).exists():
            return JsonResponse({"message": "NO_MOVIE"}, status=400)

        if Interest.objects.filter(user_id=request.user, movie_id=movie_id).exists():
            Interest.objects.delete(user_id=request.user, movie_id=movie_id)
            return JsonResponse("SUCCESS", status=204)

        return JsonResponse("SUCCESS", status=204)
    

class InterestListView(View):
    @login_decorator
    def get(self, request):
        account_id = request.user
        status = request.GET.get('status')
        
        data = {}
        if status:
            interests = Interest.objects.select_related('movie').prefetch_related('movie__star_set').filter(user_id=account_id,status=category).all()

            data = {
                'data': [{
                    'movieId': interest.movie.id,
                    'imageURL': interest.movie.main_image,
                    'title': interest.movie.name,
                    'rate': str(round(sum([star.point for star in interest.movie.star_set.all()])/interest.movie.star_set.all().count(),1)),
                    'date': f'{interest.movie.opening_at.year} . {interest.movie.country}'
                    } for interest in interests]
            }
            return JsonResponse(data, status=200)
        
        return JsonResponse(data, status=204)
