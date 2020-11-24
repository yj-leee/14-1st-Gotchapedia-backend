from django.urls import path, include

urlpatterns = [
    path('user', include('users.urls')),
    path('comment', include('comment.urls')),
    path('analysis', include('analysis.urls')),
    path('movie', include('movie.urls'))
]
