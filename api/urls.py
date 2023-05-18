from django.urls import path
from api.views import * 



urlpatterns = [
    path("add-bus/",BusApi.as_view(),name="add-bus"),
    path("update-bus/<int:id>/",BusApi.as_view(),name="update-bus"),
    path("delete-bus/<int:id>/",BusApi.as_view(),name="delete-bus"),
    path("add-journey/",JourneyRootApi.as_view(),name="add-journey"),
    path("update-journey/<int:id>/",JourneyRootApi.as_view(),name="update-journey"),
    path("delete-journey/<int:id>/",JourneyRootApi.as_view(),name="delete-journey"),
    path("book-ticket/",BookBusApi.as_view(),name="book-ticket"),
    path("delete-ticket/<int:id>/",BookBusApi.as_view(),name="delete-ticket"),
    path("update-ticket/<int:id>/",BookBusApi.as_view(),name="update-ticket"),
    path("login/",LoginView.as_view(),name="login"),
    path('search-bus/', SearchBusApi.as_view(), name='search-bus'),
    path('createuser/', CreateUserView.as_view(), name='creteuser'),
    path('getuser/', CreateUserView.as_view(), name='getuser'),
    path('updateuser/<int:id>/', CreateUserView.as_view(), name='updateuser'),
    path('deleteuser/<int:id>/', CreateUserView.as_view(), name='deleteuser'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', SendPasswordResetLinkView.as_view(), name='password-reset'),
]