from django.urls import path
from . import views

urlpatterns = [
        path("api-post-new-user/",      views.APIPostNewUser.as_view(),     name = "new-user"),
        path("api-resolve-address/",    views.APIResolveAddress.as_view(),  name = "resolve-address"),
        path("api-try-login/",          views.APITryLogin.as_view(),        name = "try-login"),

        path("api-get-chore-types/",    views.APIGetChoreTypes.as_view(),   name = "chore-types"),
        path("api-create-chore/",       views.APICreateChore.as_view(),     name = "create-chores"),

        path("api-burn-everything/",    views.APIBurnEverything.as_view(),  name = "burn-everything")
]
