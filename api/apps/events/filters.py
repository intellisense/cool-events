from django_filters import rest_framework as filters

from .models import Event


class EventFilter(filters.FilterSet):
    owner = filters.CharFilter(field_name="owner__username", lookup_expr="exact")

    class Meta:
        model = Event
        fields = ("owner",)
