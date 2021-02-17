from django.urls import path

from . import views


urlpatterns = [path("validator/", views.validation_view)]
