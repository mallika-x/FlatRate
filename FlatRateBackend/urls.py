from django.urls import path
from . import views

urlpatterns = [
        path("api-test-get/", views.APITestGet.as_view(), name = "test-get"),
]
