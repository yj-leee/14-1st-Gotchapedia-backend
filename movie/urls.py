from django.urls import path
from .views      import MovieDetailView, MoviesUserView

urlpatterns= [
    path('/movies/user', MoviesUserView.as_view()),
    path('detail/<int:movie_id>', MovieDetailView.as_view())
]