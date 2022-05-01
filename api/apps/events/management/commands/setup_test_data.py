import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.events.models import Event, EventParticipant
from apps.events.tests.factories import EventFactory, EventParticipantFactory
from apps.users.tests.factories import UserFactory

NUM_USERS = 50
NUM_EVENTS = 50
PARTICIPANTS_PER_EVENT = 15


class Command(BaseCommand):
    help = "Generates test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Flushes data and regenerates dummy data.",
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if not kwargs["confirm"]:
            message = (
                "This action will delete existing data and regenerates new data.\n"
                "Confirm action by passing --confirm flag."
            )
            raise CommandError(message)

        self.delete_old_data()
        users = self.create_users()
        events = self.create_events(users)
        self.create_events_participants(users, events)

    def delete_old_data(self):
        self.stdout.write("Deleting old data...")
        models = [get_user_model(), Event, EventParticipant]
        for m in models:
            m.objects.all().delete()

    def create_users(self):
        self.stdout.write("Creating new users...")
        users = []
        for index in range(NUM_USERS):
            username = f"testUser{index}"
            email = f"testUser{index}@localhost.com"
            user = UserFactory(
                username=username,
                email=email,
            )
            users.append(user)
        return users

    def create_events(self, users):
        self.stdout.write("Creating new events...")
        events = []
        for _ in range(NUM_EVENTS):
            owner = random.choice(users)
            event = EventFactory(owner=owner)
            events.append(event)
        return events

    def create_events_participants(self, users, events):
        self.stdout.write("Creating new event participants...")
        for event in events:
            for _ in range(PARTICIPANTS_PER_EVENT):
                # This may pick an existing participant.
                user = random.choice(users)
                EventParticipantFactory(
                    user=user,
                    event=event,
                )
