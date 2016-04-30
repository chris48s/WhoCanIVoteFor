from django.contrib import admin

from .models import Election, Post, VotingSystem


class ElectionAdmin(admin.ModelAdmin):
    list_filter = ('election_type', 'voting_system')


class PostAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'role')
    list_filter = ('organization', 'role')


admin.site.register(Election, ElectionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(VotingSystem)
