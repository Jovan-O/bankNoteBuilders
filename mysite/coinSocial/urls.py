from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'coinSocial'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("collection/int:Collection.id", views.CollectionDetailView.as_view(), name="collection"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('createaccount/', views.CreateAccountView.as_view(), name='createaccount'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
