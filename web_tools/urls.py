from django.urls import path

from . import views


urlpatterns = [path("tools/validator/", views.validation_view),
               path('tools/', views.tool_list_view),
               path("", views.index)]
