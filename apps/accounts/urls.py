from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("keys/", views.RSKeyPairView.as_view(), name="keys"),
    path("locations/", views.UserGeoDataView.as_view(), name="geo_data"),
    path("sessions/", views.UserSessionView.as_view(), name="sessions"),
]
