from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from events.models import RSVP, Event
from notification.models import Notification
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()


@receiver(post_save, sender=Event)
def event_created_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New event '{instance.title}' has been created."
        category = "Event Creation"

        channel_layer = get_channel_layer()
        organizer_channel_name = f"channel_{instance.organizer.username}"
        async_to_sync(channel_layer.group_send)(
            "broadcast",
            {
                'type': 'organizer_message',
                'message': f'You\'ve created a new event {instance.title}',
                'organizer': instance.organizer.username,
                'created_at': '',
            }
        )

        Notification.objects.create(
            user=instance.organizer, message=message, category=category)


@receiver(pre_save, sender=Event)
def cache_previous_values(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Event.objects.get(pk=instance.pk)

        instance._cached_fields = {
            'date': old_instance.date,
            'location': old_instance.location,
            'time': old_instance.time
        }


@receiver(post_save, sender=Event)
def event_updated_notification(sender, instance, created, **kwargs):
    if not created:
        if (instance._cached_fields['date'] != instance.date) or \
            (instance._cached_fields['location'] != instance.location) or \
                (instance._cached_fields['location'] != instance.location):
            registered_users = instance.registered_users.all()

            for user in registered_users:
                message = f"The event, '{instance.title}', you've registered for has been updated. View the changes."
                Notification.objects.create(
                    user=user, message=message, category='Event Updates ')


@receiver(post_save, sender=RSVP)
def rsvp_notification(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        user = instance.user

        organizer = event.organizer
        organizer_message = f"{user.username} has rsvp for your event, '{event.title}'."
        Notification.objects.create(
            user=organizer, message=organizer_message, category='RSVP Notifications')

        user_message = f"You've successfully rsvp for the event, '{event.title}'."
        Notification.objects.create(
            user=user, message=user_message, category='RSVP Notifications')


@receiver(m2m_changed, sender=Event.registered_users.through)
def event_registration_changed(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            message = f"You've registered for the event, '{instance.title}'."
            Notification.objects.create(
                user=user, message=message, category='Registration Notifications')

        organizer = instance.organizer
        organizer_message = f"You have new event registration."
        Notification.objects.create(
            user=organizer, message=organizer_message, category='Registration Notifications')


@receiver(m2m_changed, sender=Event.invited_users.through)
def event_invitation_notification(sender, instance, action, model, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            message = f"You've been invited to the event, '{instance.title}'."
            Notification.objects.create(
                user=user, message=message, category='Invitation Notifications')
