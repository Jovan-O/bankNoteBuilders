from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Collection, Item

# Create your views here.

class IndexView(generic.ListView):
    template_name = "coinSocial/index.html"
    collection_list = Collection.objects.all()

    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.all()


# TODO: Figure out to link all items in a collection to a variable to access them in the views
class CollectionView(generic.ListView):
    template_name = "coinSocial/index.html"
    coin_list = Item.objects.filter(collectionID)

    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.all()

# TODO: Create more views
