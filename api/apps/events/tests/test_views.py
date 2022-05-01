import datetime

from django.urls import reverse
from django.utils import timezone

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.events.constants import ALREADY_ATTENDING_EVENT
from apps.events.views import EventParticipantViewSet, EventViewSet
from apps.users.tests.factories import UserFactory

from .factories import EventFactory, EventParticipantFactory


@pytest.fixture
def another_user():
    return UserFactory(username="testUser", email="testUser@test.com")


@pytest.mark.django_db
class TestEventViewSet:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.request_factory = APIRequestFactory()
        self.event = EventFactory()
        self.start_date = timezone.now()
        self.user = UserFactory()
        self.view = EventViewSet

        self.detail_endpoint = reverse(
            "events:event-detail", kwargs={"pk": self.event.pk}
        )
        self.list_endpoint = reverse("events:event-list")

    def get_payload(self, **kwargs):
        payload = {
            "title": "New Event",
            "description": "This is a test event.",
            "start_date": self.start_date.isoformat(),
        }
        payload.update(kwargs)
        return payload

    def test_create(self):
        payload = self.get_payload()
        request = self.request_factory.post(self.detail_endpoint, payload)
        force_authenticate(request, user=self.user)
        detail_view = self.view.as_view({"post": "create"})
        response = detail_view(request)
        assert response.status_code == status.HTTP_201_CREATED
        event = response.data
        assert set(event.keys()) == {
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

    def test_put(self):
        new_event_title = "Updated title."
        payload = self.get_payload(title=new_event_title)
        request = self.request_factory.put(self.detail_endpoint, payload)
        force_authenticate(request, user=self.user)
        update_view = self.view.as_view({"put": "update"})
        response = update_view(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        event = response.data
        assert event["title"] == new_event_title

    def test_patch(self):
        new_event_title = "Updated title."
        payload = {"title": new_event_title}
        request = self.request_factory.patch(self.detail_endpoint, payload)
        force_authenticate(request, user=self.user)
        partial_update_view = self.view.as_view({"patch": "partial_update"})
        response = partial_update_view(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        event = response.data
        assert event["title"] == new_event_title

    def test_retrieve(self):
        request = self.request_factory.get(self.detail_endpoint)
        force_authenticate(request, user=self.user)
        detail_view = self.view.as_view({"get": "retrieve"})
        response = detail_view(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(self.event.pk)

    def test_list(self):
        request = self.request_factory.get(self.list_endpoint)
        force_authenticate(request, user=self.user)
        list_view = self.view.as_view({"get": "list"})
        response = list_view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_destroy(self):
        request = self.request_factory.delete(self.detail_endpoint)
        force_authenticate(request, user=self.user)
        delete_view = self.view.as_view({"delete": "destroy"})
        response = delete_view(request, pk=self.event.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_update(self):
        new_start_date = self.start_date + datetime.timedelta(days=1)
        payload = {
            "title": "Event title updated",
            "description": "Event description updated.",
            "start_date": new_start_date.isoformat(),
        }

        request = self.request_factory.put(self.detail_endpoint, payload)
        force_authenticate(request, user=self.user)
        update_view = self.view.as_view({"put": "update"})
        response = update_view(request, pk=self.event.pk)

        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["title"] == payload["title"]
        assert data["description"] == payload["description"]
        assert data["start_date"] == payload["start_date"].replace("+00:00", "Z")

    def test_partial_update(self):
        payload = {"title": "Event title updated"}
        request = self.request_factory.patch(self.detail_endpoint, payload)
        force_authenticate(request, user=self.user)
        update_view = self.view.as_view({"patch": "partial_update"})
        response = update_view(request, pk=self.event.pk)

        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["title"] == payload["title"]


@pytest.mark.django_db
class TestEventParticipantViewSet:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.request_factory = APIRequestFactory()
        self.user = UserFactory()
        self.event = EventFactory()
        self.view = EventParticipantViewSet

        self.list_endpoint = reverse(
            "events:event-participants-list", kwargs={"event_pk": self.event.pk}
        )
        self.create_endpoint = reverse(
            "events:event-participants-list", kwargs={"event_pk": self.event.pk}
        )

    def get_detail_endpoint(self, participant):
        return reverse(
            "events:event-participants-detail",
            kwargs={
                "event_pk": self.event.pk,
                "pk": participant.pk,
            },
        )

    def test_list(self, another_user):
        # Add one more participant other than default owner
        EventParticipantFactory(user=another_user, event=self.event)
        request = self.request_factory.get(self.list_endpoint)
        force_authenticate(request, user=self.user)
        list_view = self.view.as_view({"get": "list"})
        response = list_view(request, event_pk=self.event.pk)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_create(self, another_user):
        request = self.request_factory.post(self.create_endpoint)
        force_authenticate(request, user=another_user)
        attend_view = self.view.as_view({"post": "create"})
        response = attend_view(request, event_pk=self.event.pk)

        assert response.status_code == status.HTTP_201_CREATED
        participant = response.data
        assert set(participant.keys()) == {"id", "username"}
        assert participant["username"] == another_user.username

    def test_already_attending(self):
        request = self.request_factory.post(self.create_endpoint)
        force_authenticate(request, user=self.user)
        attend_view = self.view.as_view({"post": "create"})
        response = attend_view(request, event_pk=self.event.pk)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        errors = response.data
        assert len(errors) == 1
        assert errors[0].code == ALREADY_ATTENDING_EVENT

    def test_destroy(self, another_user):
        """Test remove participant as an event owner."""
        participant = EventParticipantFactory(user=another_user, event=self.event)
        endpoint = self.get_detail_endpoint(participant)
        request = self.request_factory.delete(endpoint)
        force_authenticate(request, user=self.user)
        destroy_view = self.view.as_view({"delete": "destroy"})
        response = destroy_view(request, event_pk=self.event.pk, pk=participant.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_destroy_as_participant(self, another_user):
        """Test remove as participant."""
        participant = EventParticipantFactory(user=another_user, event=self.event)
        endpoint = self.get_detail_endpoint(participant)
        request = self.request_factory.delete(endpoint)
        force_authenticate(request, user=another_user)
        destroy_view = self.view.as_view({"delete": "destroy"})
        response = destroy_view(request, event_pk=self.event.pk, pk=participant.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_destroy_as_common_user(self, another_user):
        participant = self.event.participants.first()
        endpoint = self.get_detail_endpoint(participant)
        request = self.request_factory.delete(endpoint)
        force_authenticate(request, user=another_user)
        destroy_view = self.view.as_view({"delete": "destroy"})
        response = destroy_view(request, event_pk=self.event.pk, pk=participant.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_cannot_withdraw(self):
        """Test event owner cannot be removed as participant."""
        participant = self.event.participants.first()
        assert participant.user == self.event.owner
        endpoint = self.get_detail_endpoint(participant)
        request = self.request_factory.delete(endpoint)
        force_authenticate(request, user=self.user)
        destroy_view = self.view.as_view({"delete": "destroy"})
        response = destroy_view(request, event_pk=self.event.pk, pk=participant.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN
