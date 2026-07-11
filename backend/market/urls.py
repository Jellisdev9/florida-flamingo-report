from django.urls import path
from . import views

urlpatterns = [
    path("market/metrics/", views.market_metrics),
    path("market/neighborhoods/", views.neighborhood_intel),
    path("market/fastest-growing/", views.fastest_growing),
    path("agents/top/", views.top_agents),
]
