from django.urls import path
from .views      import StarView, StarDetailView

urlpatterns= [
    path('/star/', StarView.as_view()),
    path('/star/<int:movie_id>', StarDetailView.as_view())
]
