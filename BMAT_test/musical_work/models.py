from django.db import models


class MusicalWork(models.Model):
    title = models.CharField(max_length=64)
    contributors = models.CharField(max_length=256)
    iswc = models.CharField(max_length=16)
    source = models.CharField(max_length=256)

    def __str__(self):
        return self.title
