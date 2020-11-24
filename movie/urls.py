from django.urls import path
from .views      import InterestView, InterestListView

urlpatterns= [
    path('/interests', InterestListView.as_view()),
    path('/<int:movie_id>/interest', InterestView.as_view()),
]
