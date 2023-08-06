# coding=utf-8
from django.urls.conf import path
from edc_pharmacy_dashboard.views import HomeView
from edc_pharmacy_dashboard.views.listboard_views import PrescribeListboardView


app_name = "edc_pharmacy_dashboard"

urlpatterns = [
    path(
        r"rx/prescribe/",
        PrescribeListboardView.as_view(),
        name="prescribe_listboard_url",
    ),
    path(
        r"rx/dispense/", PrescribeListboardView.as_view(), name="dispense_listboard_url"
    ),
    path("home/", HomeView.as_view(), name="home_url"),
    path("", HomeView.as_view(), name="home_url"),
]
