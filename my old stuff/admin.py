from django.contrib import admin
from .models import Admin

# Register your models here.


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    listDisplay = ('user', 'role')
    listFilter = ('role',)
