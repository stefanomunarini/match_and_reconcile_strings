from rest_framework import viewsets

from musical_work.models import MusicalWork
from musical_work.serializers import MusicalWorkSerializer


class MusicalWorkViewSet(viewsets.ModelViewSet):
    lookup_field = "iswc"
    queryset = MusicalWork.objects.all()
    serializer_class = MusicalWorkSerializer

