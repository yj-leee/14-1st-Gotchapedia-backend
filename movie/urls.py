from django.urls import path
from movie.views import SearchView


urlpatterns = [
    path("", SearchView.as_view()),
]
