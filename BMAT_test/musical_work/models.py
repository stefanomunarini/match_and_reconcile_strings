from django.db import models


class MusicalWork(models.Model):
    title = models.CharField(max_length=64)
    contributors = models.CharField(max_length=128)
    iswc = models.CharField(max_length=16)

    # class Meta:
    #     unique_together = (("iswc", "source", 'source_id'),)

    def __str__(self):
        return self.title
