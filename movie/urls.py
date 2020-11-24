from django.urls import path
from .views      import MovieInfoView, MovieDetailView, MoviesUserView

urlpatterns= [
    path('/movies/user', MoviesUserView.as_view()),
    path('detail/<int:movie_id>', MovieDetailView.as_view()),
    path('<int:movie_id>', MovieInfoView.as_view())
]