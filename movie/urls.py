from django.urls import path

from .views      import (
    MovieDetailView,
    MovieInfoView,
    MoviesUserView,
    SearchView,
    InterestView,
    InterestListView
)

urlpatterns= [
    path('/user', MoviesUserView.as_view()),
    path('', SearchView.as_view()),
    path('/<int:movie_id>', MovieInfoView.as_view()),
    path('/<int:movie_id>/detail', MovieDetailView.as_view()),
    path('/<int:movie_id>/interest', InterestView.as_view()),
    path('/interests', InterestListView.as_view())
]
