from django.contrib import admin

from .models import Person, PersonPost

admin.site.register(Person)
admin.site.register(PersonPost)
