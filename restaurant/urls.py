from django.urls import path

from restaurant.views import index


app_name = "restaurant"

urlpatterns = [
    path("", index, name="index"),
]
