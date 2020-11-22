from django.urls import path
from .views      import StarView

urlpatterns= [
    path('star/<int:movieId>', StarView.as_view())
]
