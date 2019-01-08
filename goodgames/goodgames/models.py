from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


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


class Image(models.Model):
    image = CloudinaryField('image')


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='game')
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='profile')
    # image = models.ForeignKey(
    #     Image, blank=True, null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # image = models.ForeignKey(
    #     Image, null=True, blank=True, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    score = models.IntegerField(default=None)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
