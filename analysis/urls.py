from django.urls    import path
from analysis.views import StarRatingView, StarView, StarDetailView, FavoriteView

urlpatterns= [
    path('/star', StarView.as_view()),
    path('/star/<int:movie_id>', StarDetailView.as_view()),
    path('/favorite', FavoriteView.as_view()),
    path('/my_star', StarRatingView.as_view())
]
