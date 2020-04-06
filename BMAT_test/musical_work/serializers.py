from rest_framework import serializers

from musical_work.models import MusicalWork


class MusicalWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalWork
        fields = ["title", "iswc", "contributors", "source"]
