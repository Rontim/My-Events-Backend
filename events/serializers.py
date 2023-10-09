from rest_framework import serializers
from .models import Event, RSVP


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventDashBoard(serializers.ModelSerializer):
    registered = serializers.SerializerMethodField()
    invited = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('title', 'organizer', 'location', 'date',
                  'time', 'registered', 'invited', 'attendees')

    def get_attendees(self, obj):
        return obj.attendees.count()

    def get_registered(self, obj):
        return obj.registered_users.count()

    def get_invited(self, obj):
        return obj.invited_users.count()


class RSVPSerializer(serializers.ModelSerializer):
    is_attending = serializers.SerializerMethodField()

    class Meta:
        model = RSVP
        fields = ['user', 'event', 'is_attending']

    def get_is_attending(self, obj):
        return obj.is_attending


class EventsDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'slug', 'date', 'time')
