import secrets

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class RecipePost(models.Model):
    recipe_name = models.CharField(max_length=70)
    short_description = models.CharField(max_length=200)
    ingredients = models.CharField(max_length=300, null=True)
    cooking_directions = models.TextField(max_length=3000)
    cooking_tips = models.TextField(max_length=500)
    cooking_time = models.IntegerField()
    preparation_time = models.IntegerField()
    recipe_images = models.ImageField(upload_to='media/%Y/%m/%d')
    recipe_datePosted = models.DateTimeField(default=timezone.now)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(choices=STATUS, default=0)

    # If the user is deleted, all their post will be deleted too.

    def __str__(self):
        return self.recipe_name
