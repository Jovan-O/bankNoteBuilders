from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Collection, Item

from django.shortcuts import render, get_object_or_404
from .models import Post

def view_post(request, post_id):
    post = get_object_or_404(Post, postID=post_id)
    return render(request, 'coinSocial/view_post.html', {'post': post})


# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "coinSocial/index.html"
    collection_list = Collection.objects.all()

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
        context['coin_list'] = Item.objects.filter(collection=self.collection)
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
