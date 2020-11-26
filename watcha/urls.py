from django.urls import path, include

urlpatterns = [
    path('user', include('users.urls')),
    path('analysis', include('analysis.urls')),
    path('movie', include('movies.urls')),
    path('comment', include('comments.urls'))
]
