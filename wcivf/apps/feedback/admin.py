from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ('found_useful',)
    list_display = ('found_useful', 'comments',)
    readonly_fields = Feedback._meta.get_all_field_names()

admin.site.register(Feedback, FeedbackAdmin)
