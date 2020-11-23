from django.urls import path
from analysis.views import StarRatingView

urlpatterns = [
    path("/my_star", StarRatingView.as_view()),
]
