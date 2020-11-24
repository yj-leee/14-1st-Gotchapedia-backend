from django.urls import path

from .views import MovieInfoView, MovieUserView, SearchView, InterestView, InterestListView

urlpatterns= [
    path("", SearchView.as_view()),
    path('<int:movie_id>', MovieInfoView.as_view())
    path('/movies/user', MoviesUserView.as_view()),
    path('detail/<int:movie_id>', MovieDetailView.as_view()),
    path('/interests', InterestListView.as_view()),
    path('/<int:movie_id>/interest', InterestView.as_view()),
]
