from django.db import models

class Star(models.Model):
    point       = models.DecimalField(max_digits=2, decimal_places=1)
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie       = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta:
        db_table = 'stars'

class UserLog(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie       = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    created_at  = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_log'

