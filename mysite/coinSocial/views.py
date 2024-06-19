from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import generic
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Collection, Item
from .forms import CollectionForm

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "coinSocial/index.html"


class CollectionDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'coinSocial/collection.html'
    login_url = 'coinSocial:login'

    def dispatch(self, request, *args, **kwargs):
        collection_id = self.kwargs.get('collectionID')
        self.collection = get_object_or_404(Collection, collectionID=collection_id)

        # Check if the logged-in user is the owner of the collection
        if self.request.user != self.collection.owner:
            return HttpResponseForbidden("You do not own this collection")

        return super().dispatch(request, *args, **kwargs)
# TODO: Figure out to link all items in a collection to a variable to access them in the views
class CollectionView(generic.ListView):
    template_name = "coinSocial/collection.html"
    coin_list = Item.objects.all()

    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coin_list'] = Item.objects.filter(collection=self.collection)
        context['collection'] = self.collection
        return context


# TODO: Create more views

class PostView(generic.ListView):
    template_name = "coinSocial/post.html"

# This used to be a template view
class DashboardView(generic.ListView, LoginRequiredMixin):
    template_name = "coinSocial/dashboard.html"
    login_url = 'coinSocial:login'
    redirect_field_name = 'next'

    collection_list = Collection.objects.all()

class AccountCreationView(generic.ListView):
    template_name = "coinSocial/registration/createaccount.html"

    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.filter(owner=self.request.user)


def makecollections(request, collectionID):
    collection = get_object_or_404(Collection, id=collectionID)
    items = Item.objects.filter(collection=collection)  # Filter items by collection

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('coinSocial:login')
    template_name = 'registration/register.html'


class CollectionCreateView(generic.CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'coinSocial/create_collection.html'
    success_url = reverse_lazy('coinSocial:dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the current user
        return super().form_valid(form)

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
    success = False
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            new_collection = form.save(commit=False)
            new_collection.owner = request.user  # Assign current user as the owner
            new_collection.save()
            success = True
    else:
        form = CollectionForm()
    return render(request, 'coinSocial/create_collection.html', {'form': form, 'success': success})


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['collection', 'name', 'value', 'condition', 'origin', 'description', 'dateOfIssue', 'frontImg',
                  'backImg']


def create_item(request):
    success = False
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = ItemForm()
    return render(request, 'coinSocial/post.html', {'form': form, 'success': success})