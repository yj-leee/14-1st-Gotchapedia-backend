from django.db import models

class Comment(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie    = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    comment  = models.ForeignKey(
        'Comment',
        on_delete    = models.CASCADE,
        related_name = 'main_comment'
    )
    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment  = models.ForeignKey('comment.Comment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

