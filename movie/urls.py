from django.urls import path
from .views      import MovieDetailView

urlpatterns= [
    path('detail/<int:movieId>', MovieDetailView.as_view())
]
