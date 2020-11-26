from django.urls import path

from .views      import (
    MovieDetailView,
    MovieInfoView,
    MoviesUserView,
    SearchView,
    InterestView,
    InterestListView,
    ReplyView,
    ReplyListView,
    CommentView,
    CommentListView,
    CommentLikeView
)

urlpatterns= [
    path('/user', MoviesUserView.as_view()),
    path('', SearchView.as_view()),
    path('/<int:movie_id>', MovieInfoView.as_view()),
    path('/<int:movie_id>/detail', MovieDetailView.as_view()),
    path('/<int:movie_id>/interest', InterestView.as_view()),
    path('/interests', InterestListView.as_view()),
    path('', CommentView.as_view()),
    path('/<int:movie_id>', CommentView.as_view()),
    path('/list/<int:movie_id>', CommentListView.as_view()),
    path('/like', CommentLikeView.as_view()),
    path('/like/<int:comment_id>', CommentLikeView.as_view()),
    path('/<int:comment_id>/reply', ReplyListView.as_view()),
    path('/reply/<int:reply_id>', ReplyView.as_view())
]
