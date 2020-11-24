from django.urls import path
from .views      import InterestView, InterestListView

urlpatterns= [
    #path('/movies/user', MoviesUserView.as_view()),
    path('/interests', InterestListView.as_view()), #GET
    path('/<int:movie_id>/interest', InterestView.as_view()),# GET/POST/FETCH/DELETE
]
