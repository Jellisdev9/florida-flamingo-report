from django.urls import path
from . import views

urlpatterns = [
    path("sales/", views.NotableSaleListView.as_view()),
    path("sales/featured/", views.featured_sale),
    path("sales/top-closings/", views.top_closings),
]
