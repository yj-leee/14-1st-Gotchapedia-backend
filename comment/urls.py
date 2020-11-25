from django.urls import path
from .views      import CommentView, CommentListView, CommentLikeView 

urlpatterns= [
    path('/', CommentView.as_view()),
    path('/<int:movie_id>', CommentView.as_view()),
    path('/list/<int:movie_id>', CommentListView.as_view()),
    path('/like', CommentLikeView.as_view()),
    path('/like/<int:comment_id>', CommentLikeView.as_view())
]