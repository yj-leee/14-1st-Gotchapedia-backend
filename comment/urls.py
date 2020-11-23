from django.urls import path
from .views      import CommentLikeView

urlpatterns= [
    path('like/', CommentLikeView.as_view()),
    path('like/<int:comment_id>', CommentLikeView.as_view())
]
