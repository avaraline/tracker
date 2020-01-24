from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/games/", views.GamesAPI.as_view(), name="api-games"),
    path("admin/", admin.site.urls),
]
