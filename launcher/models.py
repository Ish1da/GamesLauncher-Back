from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=128, blank=False)