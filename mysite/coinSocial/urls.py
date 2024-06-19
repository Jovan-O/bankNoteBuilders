from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'coinSocial'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("collection/<int:collectionID>/", views.CollectionDetailView.as_view(), name="collection"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('create_collection/', views.CollectionCreateView.as_view(), name='create_collection'),
]
