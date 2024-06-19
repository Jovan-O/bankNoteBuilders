from django.contrib import admin
from .models import Admin

# Register your models here.


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    listDisplay = ('user', 'role')
    listFilter = ('role',)


from django.contrib import admin
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('collectionID', 'nameUG', 'owner', 'publicUG')
    search_fields = ('nameUG', 'owner__username')  # Allow searching by collection name and owner username
    list_filter = ('publicUG', 'owner')  # Add filters for public status and owner
    ordering = ('collectionID',)  # Default ordering by collection ID

admin.site.register(Collection, CollectionAdmin)
