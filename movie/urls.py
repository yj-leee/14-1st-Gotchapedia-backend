from django.urls import path
from .views      import StarView

urlpatterns= [
    path('<int:movieId>/star', StarView.as_view())
]
