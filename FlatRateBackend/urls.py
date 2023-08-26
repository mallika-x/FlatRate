from django.urls import path
from . import views

urlpatterns = [
        path("api-post-new-user/",      views.APIPostNewUser.as_view(),     name = "new-user"),
        path("api-resolve-address/",    views.APIResolveAddress.as_view(),  name = "resolve-address"),
        path("api-try-login/",          views.APITryLogin.as_view(),        name = "try-login"),

        path("api-get-chore-types/",    views.APIGetChoreTypes.as_view(),   name = "chore-types"),
        path("api-create-chore/",       views.APICreateChore.as_view(),     name = "create-chores"),
        path("api-get-user-chores/",    views.APIGetUserChores.as_view(),   name = "get-user-chores"),
        path("api-get-others-chores/",  views.APIGetOthersChores.as_view(), name = "get-others-chores"),
        path("api-complete-chore/",     views.APICompleteChore.as_view(),   name = "complete-chore"),
        path("api-get-chore-details/",  views.APIGetChoreDetails.as_view(), name = "chore-details"),
        path("api-get-chore-history/",  views.APIGetChoreHistory.as_view(), name = "chore-history"),

        path("api-get-flatmates/",      views.APIGetFlatmates.as_view(),    name = "get-flatmates"),
        path("api-change-lease/",       views.APIChangeLease.as_view(),     name = "change-lease"),

        path("api-get-tallies/",        views.APIGetTallies.as_view(),      name = "get-tallies"),
        path("api-get-socialcredits/",  views.APIGetSocialCredits.as_view(),name = "get-social-credits"),

        path("api-burn-everything/",    views.APIBurnEverything.as_view(),  name = "burn-everything")
]
