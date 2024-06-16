from django.urls import path
from . import views

app_name = 'coinSocial'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("collection/<int:collectionID>/", views.CollectionView.as_view(), name="collection"),
]
