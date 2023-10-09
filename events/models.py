from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils import timezone, text

User = get_user_model()


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    max_capacity = models.PositiveIntegerField(default=0)
    registered_users = models.ManyToManyField(
        User, related_name='registered_events', blank=True)
    invited_users = models.ManyToManyField(
        User, related_name='invited_events', blank=True)
    rsvps = models.ManyToManyField(
        User, through='RSVP', related_name='rsvp_events', blank=True)
    attendees = models.ManyToManyField(
        User, related_name='attended_events', blank=True)
    ticket_price = models.DecimalField(
        decimal_places=2, default=0.00, max_digits=10)

    _cached_fields = {}

    def save(self, *args, **kwargs):
        if self.date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")
        self.slug = text.slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")

    @property
    def is_full(self) -> bool:
        return self.registered_users.count() <= self.max_capacity

    @property
    def is_registered(self, user) -> bool:
        return self.registered_users.filter(email=user.email).exists()

    @property
    def total_revenue(self):
        return float(self.ticket_price * self.attendees.count())

    def __str__(self) -> str:
        return f"{self.title} at {self.location} on {self.date}: {self.time}"


class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_attending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.event}"
