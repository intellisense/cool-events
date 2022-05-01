import datetime

from django.utils import timezone

import pytest

from apps.events.serializers import EventParticipantSerializer, EventSerializer
from apps.users.tests.factories import UserFactory

from .factories import EventFactory


@pytest.mark.django_db
class TestEventSerializer:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.serializer = EventSerializer
        self.start_date = timezone.now()
        self.user = UserFactory()

    def serializer_data(self, **kwargs):
        data = {
            "title": "New Event",
            "description": "This is a test event.",
            "start_date": self.start_date.isoformat(),
        }
        data.update(kwargs)
        return data

    def serializer_context(self):
        return {"user": self.user}

    def test_valid(self):
        data = self.serializer_data()
        context = self.serializer_context()
        serializer = self.serializer(data=data, context=context)
        assert serializer.is_valid()
        event = serializer.save()
        assert event.title == data["title"]
        assert event.description == data["description"]
        assert event.start_date.isoformat() == data["start_date"]
        assert event.participants.count() == 1
        participant = event.participants.first()
        assert participant.user == self.user

    def test_invalid(self):
        context = self.serializer_context()
        data = self.serializer_data(end_date="invalid")
        serializer = self.serializer(data=data, context=context)
        assert serializer.is_valid() is False
        errors = serializer.errors
        assert set(errors.keys()) == {"end_date"}
        assert errors["end_date"][0].code == "invalid"

    def test_invalid_with_start_date_in_past(self):
        start_date = self.start_date - datetime.timedelta(days=1)
        data = self.serializer_data(start_date=start_date)
        context = self.serializer_context()
        serializer = self.serializer(data=data, context=context)
        assert serializer.is_valid() is False
        errors = serializer.errors
        assert set(errors.keys()) == {"start_date"}
        assert errors["start_date"][0].code == "invalid"
        assert str(errors["start_date"][0]) == "The start date cannot be in the past."

    def test_invalid_with_end_date_earlier_than_start_date(self):
        end_date = self.start_date - datetime.timedelta(days=1)
        data = self.serializer_data(end_date=end_date)
        context = self.serializer_context()
        serializer = self.serializer(data=data, context=context)
        assert serializer.is_valid() is False
        errors = serializer.errors
        assert set(errors.keys()) == {"end_date"}
        assert errors["end_date"][0].code == "invalid"
        assert (
            str(errors["end_date"][0])
            == "The end date cannot be earlier than the start date."
        )

    def test_required_fields(self):
        context = self.serializer_context()
        serializer = self.serializer(data={}, context=context)
        assert serializer.is_valid() is False
        errors = serializer.errors
        assert set(errors.keys()) == {"title", "description", "start_date"}
        assert errors["title"][0].code == "required"
        assert errors["description"][0].code == "required"
        assert errors["start_date"][0].code == "required"

    def test_serialization(self):
        event = EventFactory()
        context = self.serializer_context()
        serializer = self.serializer(context=context)
        data = serializer.to_representation(event)
        assert set(data.keys()) == {
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
        }


@pytest.mark.django_db
class TestEventParticipantSerializer:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.serializer = EventParticipantSerializer
        self.event = EventFactory()
        self.participant = self.event.participants.first()

    def test_serialization(self):
        participant = self.event.participants.first()
        serializer = self.serializer()
        data = serializer.to_representation(participant)
        assert set(data.keys()) == {"id", "username"}
