from django.contrib import admin
from .models import Admin
from .models import Collection

# Register your models here.


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    listDisplay = ('user', 'role')
    listFilter = ('role',)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'public')
    search_fields = ('nameUG', 'owner__username')  # Allow searching by collection name and owner username
    list_filter = ('public', 'owner')  # Add filters for public status and owner
    ordering = ('id',)  # Default ordering by collection ID


admin.site.register(Collection, CollectionAdmin)
