from django.urls import path
from .views      import MovieInfoView

urlpatterns= [
    path('<int:movieId>', MovieInfoView.as_view())
]
