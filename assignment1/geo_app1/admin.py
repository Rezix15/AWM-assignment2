from django.contrib import admin
from .models import Hotel, Restaurant, Library, Park, Profile

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Restaurant)
admin.site.register(Library)
admin.site.register(Park)
admin.site.register(Profile)
