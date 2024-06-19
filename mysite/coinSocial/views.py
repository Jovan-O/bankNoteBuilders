from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views import generic
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Collection, Item
from .forms import CollectionForm, ItemForm
from django.contrib.messages.views import SuccessMessageMixin


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_list'] = Item.objects.filter(collection=self.collection)
        context['collection'] = self.collection
        return context


class PostView(generic.ListView):
    template_name = "coinSocial/post.html"


# This used to be a template view
class DashboardView(generic.ListView, LoginRequiredMixin):
    template_name = "coinSocial/dashboard.html"
    login_url = 'coinSocial:login'
    redirect_field_name = 'next'

    collection_list = Collection.objects.all()

    def get_queryset(self):
        """Return the user's collections and list them"""
        return Collection.objects.filter(owner=self.request.user)


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('coinSocial:login')
    template_name = 'registration/register.html'


class CollectionCreateView(SuccessMessageMixin, generic.CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'coinSocial/create_collection.html'
    success_url = reverse_lazy('coinSocial:dashboard')
    success_message = "Collection created successfully!"

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the current user
        return super().form_valid(form)



def create_post(request):
    success = False
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = ItemForm()
    return render(request, 'coinSocial/post.html', {'form': form, 'success': success})


class ItemCreateView(generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'coinSocial/post.html'
    success_url = reverse_lazy('coinSocial:dashboard')

# dispatch will verify that the user is on his own collection
    def dispatch(self, request, *args, **kwargs):
        collection_id = self.kwargs.get('collectionID')
        self.collection = get_object_or_404(Collection, collectionID=collection_id)
        # Check if the logged-in user is the owner of the collection
        if self.request.user != self.collection.owner:
            return HttpResponseForbidden("You do not own this collection")

        return super().dispatch(request, *args, **kwargs)
# This will create the post
    def form_valid(self, form):
        form.instance.collection = self.collection  # Assign the current collection to the item
        form.instance.owner = self.request.user  # Assign current user as the owner
        return super().form_valid(form)