from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    collection = models.ManyToManyField(
        'Game', symmetrical=False, blank=True, related_name="collection")
    wishlist = models.ManyToManyField(
        'Game', symmetrical=False, blank=True, related_name="wishlist")

    def __str__(self):
        return self.name


class Game(models.Model):
    igdb_id = models.IntegerField(default=None)
    name = models.CharField(max_length=1000, default=None)
    cover = models.CharField(max_length=1000, default=None)

    def __str__(self):
        return str(self.igdb_id)


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='game')
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='profile')
