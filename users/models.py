from django.db import models


class User(models.Model):
    name           = models.CharField(max_length=200)
    password       = models.CharField(max_length=200)
    email          = models.EmailField(max_length=200)
    profile_image  = models.URLField(max_length=1000, null=True)
    description    = models.TextField(max_length=2000, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

