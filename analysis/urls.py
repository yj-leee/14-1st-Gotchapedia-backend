from django.urls import path
from analysis.views import StarratingView

urlpatterns = [
    path("/my_star", StarratingView.as_view()),
]
