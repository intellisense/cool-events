from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel


class Event(TimeStampedModel, UUIDModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    @property
    def owner_display(self):
        return self.owner.username

    def add_participant(self, user):
        return self.participants.get_or_create(user=user)

    def remove_participant(self, user):
        participant = self.attending(user)
        if participant:
            participant.delete()

    def attending(self, user):
        """
        Determine if `user` is attending event.
        """
        participant = None

        try:
            participant = self.participants.get(user=user)
        except EventParticipant.DoesNotExist:
            pass

        return participant

    @property
    def participants_count(self):
        return self.participants.count()

    def __str__(self):
        return self.title


class EventParticipant(TimeStampedModel, UUIDModel):
    event = models.ForeignKey(
        Event, related_name="participants", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_participating",
    )

    class Meta:
        ordering = ["-created"]
        unique_together = ("event", "user")

    def status(self):
        """
        Determine if user is attending as host or as participant.
        """
        if self.user_id == self.event.owner_id:
            return "host"
        return "participant"

    def __str__(self):
        return f"{self.event} - {self.user.username}"
