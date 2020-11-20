import json

from django.views import view
from django.http import jsonresponse

from .models import (
    comment,
    likes
)

from movie.models import (
    movie,
    picture,
    staff,
    moviestaffposition,
    genre,
    moviegenre,models
)

from users.models import user
from analysis.models import (
    star,
    interest
)

class createcommentview(view):
    def post(self, request):
        data = json.loads(request.body)

        try:
            Comment.objects.create(


        except KeyError:
            return jsonresponse({"message":"key_error"}, status=400)



class readcommentview(view):
    def get(self, request):

class updatecommentview(view):
    def post(self, request):

class deletecommentview(view):
    def get(self, request):
            
