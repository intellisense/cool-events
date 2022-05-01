from django.utils import timezone

import factory

from apps.events.models import Event, EventParticipant
from apps.users.tests.factories import UserFactory


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    owner = factory.SubFactory(UserFactory)
    title = "New Event"
    start_date = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def add_owner_as_participant(self, create, *args, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        self.participants.create(user=self.owner)


class EventParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventParticipant
        django_get_or_create = ("event", "user")

    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)
