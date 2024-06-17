from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'coinSocial'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("collection/<int:collectionID>/", views.CollectionView.as_view(), name="collection"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
