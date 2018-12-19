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
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    platform = models.CharField(max_length=40)

    def __str__(self):
        return self.title


# class Reviews(models.Model):
#     one_star = 1
#     two_star = 2
#     three_star = 3
#     four_star = 4
#     five_star = 5
#     review_choices = (
#         (one_star, 'One Star'),
#         (two_star, 'Two Star'),
#         (three_star, 'Three Star'),
#         (four_star, 'Four Star'),
#         (five_star, 'Five Star')
#     )
#     reviews = models.CharField(
#         max_length=2, choices=review_choices, default=None)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
