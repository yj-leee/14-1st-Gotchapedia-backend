from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('analysis', include('analysis.urls')),
    path('movies', include('movie.urls'))
]
