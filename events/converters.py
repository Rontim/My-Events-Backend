from django.urls import converters
from .models import Event


class SlugPrimaryKeyConverter:
    regex = r'[-\w]+'

    def to_python(self, value):
        return Event.objects.get(slug=value)

    def to_url(self, obj):
        return str(obj.slug)
