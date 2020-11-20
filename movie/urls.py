from django.urls import path
from .views      import *

urlpatterns= [
    path('star', ReadStarView.as_view()),
    path('star/create', CreateStarView.as_view()),
    path('star/update', UpdateStarView.as_view()),
    path('star/delete', DeleteStarView.as_view()),
]
