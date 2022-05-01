from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from .exceptions import AlreadyAttendingEvent
from .models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    participants_count = serializers.IntegerField(read_only=True)
    attending = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "created",
            "modified",
            "owner",
            "participants_count",
            "attending",
        )
        read_only_fields = ("id", "created", "modified")

    def __init__(self, *args, **kwargs):
        super(EventSerializer, self).__init__(*args, **kwargs)
        self.user = kwargs["context"]

    def get_owner(self, event):
        return event.owner_display

    def get_attending(self, event):
        data = {}
        participant = event.attending(self.context["user"])
        if participant:
            data.update(
                {
                    "id": participant.pk,
                    "status": participant.status(),
                }
            )
        return data

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if self.instance:
            # This is to ensure PATCH requests still go through this validation.
            if not start_date:
                start_date = self.instance.start_date
            if not end_date:
                end_date = self.instance.end_date

        if start_date and start_date.date() < timezone.now().date():
            error = "The start date cannot be in the past."
            raise serializers.ValidationError({"start_date": error})

        if start_date and end_date and end_date < start_date:
            error = "The end date cannot be earlier than the start date."
            raise serializers.ValidationError({"end_date": error})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        owner = self.context["user"]
        validated_data["owner"] = owner
        event = super(EventSerializer, self).create(validated_data)
        event.participants.create(user=owner)
        return event


class EventParticipantSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = EventParticipant
        fields = ("id", "username")
        read_only_fields = ("id",)

    def get_username(self, event_participant):
        return event_participant.user.username

    def create(self, *args):
        event = self.context["event"]
        user = self.context["user"]
        participant, created = event.add_participant(user)
        if not created:
            raise AlreadyAttendingEvent
        return participant
