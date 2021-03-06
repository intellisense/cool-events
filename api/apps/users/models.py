from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        "email",
        unique=True,
        error_messages={
            "unique": "A user is already registered with this email address",
        },
    )
