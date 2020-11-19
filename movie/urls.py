from django.urls import path
from .views import UserFavoriteView

urlpatterns = [
    path('/main',UserFavoriteView.as_view()),
]

