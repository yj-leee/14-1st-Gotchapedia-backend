from django.urls import path
from .views import MoviesUserView

urlpatterns = [
    path('/movies/user', MoviesUserView.as_view()),
]

