from django.contrib import admin

from .models import Event, EventParticipant


class EventParticipantAdminInline(admin.TabularInline):
    model = EventParticipant


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "description",
        "start_date",
        "end_date",
        "created",
        "modified",
    )
    search_fields = ("title",)
    raw_id_fields = ("owner",)
    inlines = (EventParticipantAdminInline,)


admin.site.register(Event, EventAdmin)
