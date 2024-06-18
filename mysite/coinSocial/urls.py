from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'coinSocial'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("collection/<int:collectionID>/", views.CollectionView.as_view(), name="collection"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('landing/', views.landing_page, name='landing_page'),
    path('item/', views.create_item, name='create_item'),
    path('create-collection/', views.create_collection, name='create_collection'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
