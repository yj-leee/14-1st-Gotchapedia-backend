from django.urls import path
from .views      import StarView

urlpatterns= [
    path('/star/<int:movie_id>', StarView.as_view())
]
