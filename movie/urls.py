from django.urls import path
from .views      import MovieDetailView

urlpatterns= [
    path('detail/<int:movie_id>', MovieDetailView.as_view())
]
