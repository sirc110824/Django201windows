from django.urls import path
from .views import ProfileDetailView, FollowView, ProfileUpdateView

from . import views

app_name = "profile"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]