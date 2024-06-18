from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django import forms
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


class AccountCreationView(generic.ListView):
    template_name = "coinSocial/registration/createaccount.html"

    def get_queryset(self):
        return HttpResponse("Ttest")


def makecollections(request, collectionID):
    collection = get_object_or_404(Collection, id=collectionID)
    items = Item.objects.filter(collection=collection)  # Filter items by collection

    context = {
        'collection': collection,
        'coin_list': items
    }

    print(collection.nameUG)
    print([item.name for item in items])

    return render(request, 'coinSocial/templates/collection.html', context)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


def landing_page(request):
    form = SearchForm()
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Add your search logic here, for example:
            # results = YourModel.objects.filter(field__icontains=query)
            # For demonstration, we’ll just echo the query
            results = [f"Result for '{query}'"]
    return render(request, 'coinSocial/landing.html', {'form': form, 'results': results})


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['nameUG', 'descriptionUG', 'publicUG']


def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            new_collection = form.save(commit=False)
            new_collection.owner = request.user  # Assign current user as the owner
            new_collection.save()
            print("Before Redirecting")
            return redirect('collection_created')
    else:
        form = CollectionForm()
    return render(request, 'coinSocial/Create_Collection.html', {'form': form})

def collection_created(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'coinSocial/Collection_Created.html', {'collections': collections})



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['collection', 'name', 'value', 'condition', 'origin', 'description', 'dateOfIssue', 'frontImg', 'backImg']


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_created')
    else:
        form = ItemForm()
    return render(request, 'coinSocial/post.html', {'form': form})

def item_created(request):
    return render(request, 'coinSocial/postsuccess.html')