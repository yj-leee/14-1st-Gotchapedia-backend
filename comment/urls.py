from django.urls import path
from .views      import CommentView, CommentLikeView

urlpatterns= [
    path('/like', CommentLikeView.as_view()),
    path('/like/<int:comment_id>', CommentLikeView.as_view()),
    path('/', CommentView.as_view()),
    path('/<int:movie_id>', CommentView.as_view())
]