from django.urls import path
from . import views

urlpatterns = [
        path("api-post-new-user/",     views.APIPostNewUser.as_view(),     name = "new-user"),
        path("api-try-login/",         views.APITryLogin.as_view(),        name = "try-login"),
        path("api-burn-everything/",   views.APIBurnEverything.as_view(),  name = "burn-everything")
]
