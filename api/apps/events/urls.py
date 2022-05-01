from django.urls import include, path

from rest_framework_nested import routers

from . import views

app_name = "events"
router = routers.SimpleRouter()

router.register(r"events", views.EventViewSet, basename="event")

participants_router = routers.NestedSimpleRouter(router, r"events", lookup="event")
participants_router.register(
    r"participants", views.EventParticipantViewSet, basename="event-participants"
)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(participants_router.urls)),
]
