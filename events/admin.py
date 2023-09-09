from django.contrib import admin
from .models import Event, RSVP


class RSVPInline(admin.TabularInline):
    model = RSVP
    extra = 0


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'organizer')
    list_filter = ('date', 'organizer')
    search_fields = ('title', 'description', 'organizer__username')
    inlines = [RSVPInline]


admin.site.register(Event, EventAdmin)
