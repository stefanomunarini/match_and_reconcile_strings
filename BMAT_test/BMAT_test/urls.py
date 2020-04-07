"""BMAT_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from musical_work.views import export_csv_report_view, import_csv_report_view, MusicalWorkViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"v1/musicalwork", MusicalWorkViewSet)

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="home.html")),
    url(r"", include((router.urls, "musicalwork"), namespace="musicalwork")),
    path("admin/", admin.site.urls),
    url(r"^api-auth/", include('rest_framework.urls')),
    url(r"^v1/export_csv_report/+", export_csv_report_view),
    url(r"^v1/import_csv_report_view/+", csrf_exempt(import_csv_report_view)),

]
