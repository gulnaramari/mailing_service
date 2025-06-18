from django.urls import path

from .apps import ClientsConfig

from .views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView,
    base,
    home,
)


app_name = ClientsConfig.name
urlpatterns = [
    path("", base, name='base'),
    path("", home, name="home"),
    path("clients/", ClientListView.as_view(), name="list_client"),
    path("create/", ClientCreateView.as_view(), name="create_client"),
    path("view/<int:pk>/", ClientDetailView.as_view(), name="view_client"),
    path("edit/<int:pk>/", ClientUpdateView.as_view(), name="update_client"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete_client"),
]
