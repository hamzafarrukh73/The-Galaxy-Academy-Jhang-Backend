from typing import Any

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .services import assign_user_group


@receiver(post_save, sender=User)
def handle_user_post_registration(
    sender: Any, instance: User, created: bool, **kwargs: Any
) -> None:
    if created:
        transaction.on_commit(lambda: assign_user_group(instance))
