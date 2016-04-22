from django.contrib import admin

from .models import Party


class PartyAdmin(admin.ModelAdmin):
    readonly_fields = (
        'party_id',
        'party_name',
        'emblem',
    )


admin.site.register(Party, PartyAdmin)
