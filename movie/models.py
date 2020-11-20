from django.db import models


class Movie(models.Model):
    name         = models.CharField(max_length=200)
    contry       = models.CharField(max_length=200)
    main_image   = models.URLField(max_length=1000)
    description  = models.TextField(null=True)
    opening_at   = models.DateField()
    show_time    = models.IntegerField()

    class Meta:
        db_table = 'movies'

class Picture(models.Model):
    movie  = models.ForeignKey('Movie', on_delete=models.CASCADE)
    url    = models.URLField(max_length=1000)

    class Meta:
        db_table = 'pictures'

class Staff(models.Model):
    name           = models.CharField(max_length=200)
    proflie_image  = models.URLField(max_length=1000)
    movie          = models.ManyToManyField('Movie', through='MovieStaffPosition')

    class Meta:
        db_table = 'staff'

class Position(models.Model):
    name           = models.CharField(max_length=200)

    class Meta:
        db_table = 'positions'

class MovieStaffPosition(models.Model):
    movie     = models.ForeignKey('Movie', on_delete=models.CASCADE)
    staff     = models.ForeignKey('Staff', on_delete=models.CASCADE)
    position  = models.ForeignKey('Position', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_staff_positions'

class Genre(models.Model):
    name = models.CharField(max_length=200)
    movie = models.ManyToManyField('Movie', through='MovieGenre')

    class Meta:
        db_table = 'genres'

class MovieGenre(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genre'
