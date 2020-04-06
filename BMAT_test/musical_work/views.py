import csv
import os
import time

from django.core.management import call_command
from django.http import HttpResponse, HttpResponseBadRequest
from musical_work.models import MusicalWork
from musical_work.serializers import MusicalWorkSerializer
from rest_framework import viewsets

from BMAT_test import settings


class MusicalWorkViewSet(viewsets.ModelViewSet):
    lookup_field = "iswc"
    queryset = MusicalWork.objects.all()
    serializer_class = MusicalWorkSerializer


def export_csv_report_view(request):

    if "iswc" not in request.GET:
        return HttpResponseBadRequest()

    iswc_list = request.GET.getlist("iswc")
    musical_works = MusicalWork.objects.filter(iswc__in=iswc_list)

    filepath = "{}enriched_data-{}.csv".format(settings.MEDIA_ROOT, int(round(time.time() * 1000)))

    with open(filepath, "w") as local_file:
        writer = csv.writer(local_file, quoting=csv.QUOTE_NONE)
        writer.writerow(("title", "contributors", "iswc", "source"))
        for mw in musical_works:
            writer.writerow((mw.title, mw.contributors, mw.iswc, mw.source))

    with open(filepath.format(settings.MEDIA_ROOT), "r") as saved_file:
        response = HttpResponse(saved_file, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=enriched_data.csv"

    return response


def import_csv_report_view(request):

    if request.method == "POST":

        file = request.FILES["file"]
        if not file.name.endswith(".csv"):
            return HttpResponseBadRequest()

        filepath = os.path.join(settings.BASE_DIR, "static/{}".format(file.name))
        with open(filepath, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        call_command("import_csv_data", "http://backend:8000/static/{}".format(file.name))

        return HttpResponse()

    return HttpResponseBadRequest()
