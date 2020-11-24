from django.urls import path
from .views      import MovieInfoView

urlpatterns= [
    path('<int:movie_id>', MovieInfoView.as_view())
]
