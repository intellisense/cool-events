from rest_framework.exceptions import ValidationError

from .constants import ALREADY_ATTENDING_EVENT


class AlreadyAttendingEvent(ValidationError):
    default_detail = "You are already attending this event."
    default_code = ALREADY_ATTENDING_EVENT
