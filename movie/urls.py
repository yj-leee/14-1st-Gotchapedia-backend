from django.urls import path
from .views      import ReadMovieInfoView

urlpatterns= [
    path('info/', ReadMovieInfoView.as_view())
]
