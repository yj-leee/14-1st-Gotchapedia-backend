from django.urls import path
from .views      import CommentListView

urlpatterns= [
    path('/list/<int:movie_id>', CommentListView.as_view())
]
