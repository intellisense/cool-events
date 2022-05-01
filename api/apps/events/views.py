from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .filters import EventFilter
from .models import Event, EventParticipant
from .pagination import StandardResultsSetPagination
from .permissions import CanManageEvent, CanManageEventParticipant
from .serializers import EventParticipantSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("owner").all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, CanManageEvent)
    filterset_class = EventFilter
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super(EventViewSet, self).get_serializer_context()
        context["user"] = self.request.user
        return context


class EventParticipantViewSet(viewsets.ModelViewSet):
    queryset = EventParticipant.objects.select_related("event", "user").all()
    serializer_class = EventParticipantSerializer
    permission_classes = (IsAuthenticated, CanManageEventParticipant)
    pagination_class = StandardResultsSetPagination

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs.get("event_pk"))

    def get_queryset(self):
        return self.get_event().participants.all()

    def get_serializer_context(self):
        context = super(EventParticipantViewSet, self).get_serializer_context()
        context["event"] = self.get_event()
        context["user"] = self.request.user
        return context
