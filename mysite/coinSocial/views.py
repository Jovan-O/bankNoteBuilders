from django.shortcuts import render, get_object_or_404
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
    template_name = "coinSocial/collection.html"
    coin_list = Item.objects.all()
    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collectionID')
        context['coin_list'] = Item.objects.filter(collection_id=collection_id)
        return context

# TODO: Create more views

class PostView(generic.ListView):
    template_name = "coinSocial/post.html"

def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    items = Item.objects.filter(collection=collection)  # Filter items by collection

    context = {
        'collection': collection,
        'coin_list': items
    }

    return render(request, 'coinSocial/templates/collection.html', context)