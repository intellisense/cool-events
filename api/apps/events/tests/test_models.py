import pytest

from .factories import EventFactory


class TestEvent:
    def test_str(self):
        event_title = "My cool event."
        event = EventFactory.build(title=event_title)
        assert str(event) == event_title


@pytest.mark.django_db
class TestEventParticipant:
    def test_str(self):
        event = EventFactory()
        participant = event.participants.first()
        assert str(participant) == f"{event.title} - {event.owner_display}"
