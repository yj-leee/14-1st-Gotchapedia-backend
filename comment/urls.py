from django.urls import path
from .views import ReplyView, ReplyListView

urlpatterns = [
    path("/comment/<int:comment_id>/reply", ReplyListView.as_view()),
    path("/reply/<int:reply_id>", ReplyView.as_view()),
]
