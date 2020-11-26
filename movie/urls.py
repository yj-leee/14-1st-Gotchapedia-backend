from django.urls import path

from .views      import (
    MovieDetailView,
    MovieInfoView,
    MoviesUserView,
    SearchView,
    InterestView,
    InterestListView,
    ReplyView,
    CommentView,
    CommentListView,
    CommentLikeView
)

urlpatterns= [
    path('', SearchView.as_view()),
    path('/user', MoviesUserView.as_view()),
    path('/interests', InterestListView.as_view()),
    path('/<int:movie_id>', MovieInfoView.as_view()),
    path('/<int:movie_id>/detail', MovieDetailView.as_view()),
    path('/<int:movie_id>/interest', InterestView.as_view()),
    path('/<int:movie_id>/comments', CommentListView.as_view()),
    path('/<int:movie_id>/comment', CommentView.as_view()),
    path('/<int:movie_id>/comment/<int:comment_id>', CommentView.as_view()),
    path('/comment/like', CommentLikeView.as_view()),
    path('/comment/<int:comment_id>/like', CommentLikeView.as_view()),
    path('/comment/<int:comment_id>/reply/<int:reply_id>', ReplyView.as_view())
]
