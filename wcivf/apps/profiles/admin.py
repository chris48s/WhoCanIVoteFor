from django.contrib import admin

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("person_post",)

admin.site.register(Profile, ProfileAdmin)
