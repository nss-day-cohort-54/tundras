from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    run_time = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="movies")
    date_released = models.DateField(default=date.today())
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, related_name="movies")
