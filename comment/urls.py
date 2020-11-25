from django.urls import path
from .views      import CommentView, CommentListView

urlpatterns= [
    path('/list/<int:movie_id>', CommentListView.as_view()),
    path('/', CommentView.as_view()),
    path('/<int:movie_id>', CommentView.as_view())
]