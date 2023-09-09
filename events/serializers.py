from rest_framework import serializers
from .models import Event, RSVP


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RSVPSerializer(serializers.ModelSerializer):
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = RSVP
        fields = ['user', 'event', 'is_attending']

    def get_is_attending(self, obj):
        return obj.is_attending
