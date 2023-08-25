from django.urls import path
from . import views

urlpatterns = [
        path("api-post-new-user/", views.APIPostNewUser.as_view(), name = "test-get"),
]
