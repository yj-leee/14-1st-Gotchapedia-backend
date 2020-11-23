from django.urls import path
from users.views import UserView, LoginView

urlpatterns = [
    path("", UserView.as_view()),
    path("/log-in", LoginView.as_view()),
]
